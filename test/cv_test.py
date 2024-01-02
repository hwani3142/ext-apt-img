import cv2
import datasource.transform as tf


if __name__ == "__main__":
    print(tf.readSimple().head())
    print(cv2.__version__)
