import config
from persistance import load_data, save_data
import os
import open3d as o3d
import numpy as np
import random
from PIL import Image
Image.MAX_IMAGE_PIXELS = None # enable operations on large images

fill_color = "mean_color" # "mean_color", "median_color"

def main():
    data_files = os.listdir(config.processed_meme_dir)
    
    data_files = [load_data(os.path.splitext(file)[
        0]) for file in data_files if fill_color in load_data(os.path.splitext(file)[0])]
    
    # create pointcloud
    path = "colors.xyz"
    with open(path, "w") as f:
        #region a
        # f.write("1 1 1 \n")
        # f.write("1 0 0 \n")
        # f.write("0 1 0 \n")
        # f.write("0 0 255 \n")
        # f.write("0 255 0 \n")
        # f.write("0 255 255 \n")
        # f.write("255 0 0 \n")
        # f.write("255 0 255 \n")
        # f.write("255 255 0 \n")
        # f.write("255 255 255 \n")
        #endregion
        for data in data_files:
            f.write(" ".join(str(x) for x in data[fill_color]) +"\n")

    pcd = o3d.io.read_point_cloud(path)
    # visualize(pcd)
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)

    create_image("snake.jpg", "snake_300_300_n10.png", (300,300), pcd_tree, pcd, data_files)


def create_image(src, dest, sub_img_size, pcd_tree, pcd, data_files):
    # define new image dimensions
    (sub_image_width, sub_image_height) = sub_img_size
    img = Image.open(src)
    img = img.convert("RGB")
    pixels = img.load()
    width, height = img.size

    print(f"New image size: W={width*sub_image_width} H={height*sub_image_height}")

    big_img = Image.new('RGB', (width*sub_image_width, height*sub_image_height), (255, 255, 255))

    # for each pixel, find matching meme
    for y in range(height):
        print(f"Row: {y + 1}/{height}") # some progress bar ig
        for x in range(width):
            meme = find_matching_meme(pixels[x, y], pcd_tree, pcd, data_files)

            file = "median_" + meme["id"] + ".tiff"
            path = os.path.join(config.padded_meme_dir, file)

            sub_img = Image.open(path)
            big_img.paste(sub_img, (x * sub_image_width, y * sub_image_height))

    print("Save Image (could take a while ...)")
    big_img.save(dest)


def find_matching_meme(coord, pcd_tree, pcd, data_files):
    n = 10
    k, idx, _ = pcd_tree.search_knn_vector_3d(coord, n)
    points = np.asarray(pcd.points)

    r = random.randint(0, n-1)
    color = points[idx[r]]
    roughly_equal_meme = [x for x in data_files if (np.array(x[fill_color]) == np.array(color)).all()]
    return roughly_equal_meme[0]


def visualize(pcd):

    # use coordinates as color
    np_points = np.asarray(pcd.points)
    np_colors = np_points / 255.0 
    pcd.colors = o3d.utility.Vector3dVector(np_colors)

    min_bound = np.array([0,0,0])
    max_bound = np.array([255, 255, 255])
    aabb = o3d.geometry.AxisAlignedBoundingBox(min_bound=min_bound, max_bound=max_bound)
    aabb.color = np.array([0.1, 0.1, 0.1])

    # obb = pcd.get_oriented_bounding_box()
    # obb.color = np.array([0, 0, 0])

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    # add your point cloud to the window
    vis.add_geometry(pcd)
    vis.add_geometry(aabb)

    # change point size
    render_option = vis.get_render_option()
    render_option.point_size = 10

    # run visualizer
    vis.run()

if __name__ == "__main__":
    main()
