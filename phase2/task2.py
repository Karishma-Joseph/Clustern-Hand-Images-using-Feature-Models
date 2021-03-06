"""
Multimedia Web Databases - Fall 2019: Project Group 17
Authors:
1. Sumukh Ashwin Kamath
2. Rakesh Ramesh
3. Baani Khurana
4. Karishma Joseph
5. Shantanu Gupta
6. Kanishk Bashyam

This is the CLI for task 2 of Phase 2 of the project
"""
import os
import sys

from classes.dimensionreduction import DimensionReduction
from classes.globalconstants import GlobalConstants
from utils.imageviewer import show_images
from utils.inputhelper import get_input_k, get_input_feature_extractor_model, \
    get_input_dimensionality_reduction_model, get_input_folder, get_input_image, get_input_m
from utils.model import Model

model_interact = Model()
global_constants = GlobalConstants()


def main():
    """Main function for the task 2"""
    feature_extraction_model = get_input_feature_extractor_model()
    dimension_reduction_model = get_input_dimensionality_reduction_model()
    k_value = get_input_k()
    folder = get_input_folder()
    image_name = get_input_image(folder)
    m_value = get_input_m()

    print(global_constants.LINE_SEPARATOR)
    print("User Inputs summary")
    print(global_constants.LINE_SEPARATOR)
    print("Feature Extraction Model: {}\nDimensionality Reduction Model: {}\nk-value: {}\nFolder: {}\n"
          "Image: {}\nm-value: {}".format(feature_extraction_model, dimension_reduction_model, k_value, folder,
                                          image_name, m_value))
    print(global_constants.LINE_SEPARATOR)

    if dimension_reduction_model != "NMF":
        dist_func = "euclidean"
    elif feature_extraction_model in ["CM", "LBP"]:
        dist_func = "nvsc1"
    else:
        dist_func = "euclidean"
        # dist_func = "cosine"
        # dist_func = "chebyshev"
        # dist_func = "manhattan"
        # dist_func = "chi_square"
        # dist_func = "euclidean"

    # Saves the returned model
    filename = feature_extraction_model + "_" + dimension_reduction_model + "_" + str(k_value)
    model = model_interact.load_model(filename=filename)

    if not model:
        print("Please run Task 1 for {}, {} and {}".format(feature_extraction_model, dimension_reduction_model, k_value))
        sys.exit(1)

    # Compute the reduced dimensions for the new query image
    dim_reduction = DimensionReduction(feature_extraction_model, dimension_reduction_model, k_value)
    # print(dim_reduction.compute_query_image(model, folder, image_name))
    result = dim_reduction.find_m_similar_images(model, m_value, folder, image_name, dist_func)
    print(global_constants.LINE_SEPARATOR)
    print("Similar Images")
    print(global_constants.LINE_SEPARATOR)
    for rec in result:
        print(rec)
    print(global_constants.LINE_SEPARATOR)
    title = {
        "Feature Extraction": feature_extraction_model,
        "Dimensionality Reduction": dimension_reduction_model,
        "k": k_value,
        "Distance": dist_func
    }
    show_images(os.path.abspath(os.path.join(folder, image_name)), result, title)


if __name__ == "__main__":
    main()
