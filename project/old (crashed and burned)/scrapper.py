import os
import time
import selenium
from selenium import webdriver
import cv2 as cv
import requests
import numpy as np
from PIL import Image

DRIVER_PATH = "./chromedriver"


class FaceScraper:

    def __init__(self, path_to_driver=DRIVER_PATH, path_to_face_model="./face_detector.xml",
                 path_to_eye_model="./eye_detector.xml"):

        self._img_urls = dict()
        self._images = dict()
        self._wdriver_path = DRIVER_PATH
        self._face_cascade = cv.CascadeClassifier()
        self._eye_cascade = cv.CascadeClassifier()

        # -- 1. Load the cascades
        if not self._face_cascade.load(path_to_face_model):
            print('--(!)Error loading face cascade')
            exit(0)
        if not self._eye_cascade.load(path_to_eye_model):
            print('--(!)Error loading eye cascade')
            exit(0)

    def getImgUrls(self, search_terms=["smiling", "sad", "surprised", "angry", "neutral", "disgust"],
                   max_num_links=100, ):
        if (search_terms != None):
            self._search_terms = search_terms

        wd = webdriver.Chrome(executable_path=DRIVER_PATH)

        for term in self._search_terms:
            self._img_urls[term] = self._fetch_image_urls(term, wd, max_links_to_fetch=max_num_links,
                                                          sleep_between_interactions=0.1)

        wd.quit()

    def extractFaces(self):
        if len(self._img_urls.keys()) == 0:
            raise ValueError("No images in object.")

        for label in self._img_urls.keys():
            results = []
            print("Extracting label: %s\n" % label)

            i = -1
            for url in self._img_urls[label]:
                try:
                    i += 1
                    print("  Extracting label: {} no: {}; url: {}".format(label, i, url))
                    resp = requests.get(url, stream=True).raw
                    print("\tGrabbed image from server")
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    print("\tConverted to an array")
                    image = cv.imdecode(image, cv.IMREAD_COLOR)
                    print("\tDecoded image")

                    print("\tGetting faces")
                    for face in self._detectFace(image):
                        results.append(face)
                except:
                    print("    error: couldn't extract faces for url")
                    continue

            self._images[label] = results

    def saveCropped(self, parent_dir=os.getcwd(), image_type="png"):
        if len(self._images.keys()) == 0:
            raise ValueError("No images in object.")

        path_to_srcapped = parent_dir + "/scrapped_images"
        i = 1
        while (os.path.exists(path_to_srcapped)):
            path_to_srcapped = path_to_srcapped + "_" + str(i)
            i += 1
        print("Saving to %s" % path_to_srcapped)
        os.mkdir(path_to_srcapped)
        for label in self._images:
            try:
                print("Exteracting for %s" % label)
                labelDir = path_to_srcapped + "/" + label
                os.mkdir(labelDir)
            except OSError:
                print("Unable to write images under %s label\n" % label)
                continue

            for index in range(len(self._images[label])):
                image_path = labelDir + "/" + label + "_" + str(index) + "." + image_type
                cv.imwrite(image_path, self._images[label][index])
                try:
                    print("Progress: %.2f%" % 100 * index / len(self._images[label]))
                except:
                    continue

    def _detectFace(self, frame):
        print("\t  preprocessing image", end="... ")
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.equalizeHist(frame_gray)
        # -- Detect faces and eyes
        print("Detecting faces image", end="... ")
        faces = self._face_cascade.detectMultiScale(frame_gray)
        eyes = self._eye_cascade.detectMultiScale(frame_gray)
        print("veryfiying", end="... ")
        real_faces = []
        for (x, y, w, h) in faces:
            # x_min, y_min, x_max, y_max = x, y, x + w, y + h
            # for (x_eye, y_eye, w_eye, h_eye) in eyes:
            #     if (x_min <= x_eye and x_eye <= x_max) and (y_min <= y_eye and y_eye <= y_max):
            #         real_faces.append((x, y, w, h))
            #         break
            real_faces.append((x, y, w, h))
            if len(real_faces) > 5:
                break
        print("\t  Done!")
        return [frame[y:y + h, x:x + w] for (x, y, w, h) in real_faces]

    # source
    # https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
    def _fetch_image_urls(self, query, wd, max_links_to_fetch, sleep_between_interactions=1):
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # build the google query

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            print("Found: {0} search results. Extracting links from {1}:{0}".format(number_results, results_start))

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print("Found: {} image links, done!".format(len(image_urls)))
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(15)
                # return image_urls
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
                else:
                    return image_urls

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        return image_urls


if __name__ == "__main__":
    list_of_search_terms = [
        "people at weddings",
        "depression human face",
        "people at senate hearing",
        "disgusted face",
        "people shocked"
    ]

    getFaces = FaceScraper()
    getFaces.getImgUrls(["human angry"], 200)
    getFaces.extractFaces()
    getFaces.saveCropped()
    getFaces.getImgUrls(["angry"], 200)
    getFaces.extractFaces()
    getFaces.saveCropped()
    getFaces.getImgUrls(["anger face"], 200)
    getFaces.extractFaces()
    getFaces.saveCropped()