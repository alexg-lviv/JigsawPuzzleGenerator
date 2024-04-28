import numpy as np
from PIL import Image
from PuzzleGenerator import PuzzleGenerator
from Algorithms.Splitters.RectSplitter import RectSplitter
from Algorithms.Splitters.HexSpliter import HexSplitter
from Algorithms.Splitters.VoronoiSplitter import VoronoiSplitter
from Algorithms.Splitters.SuperpixelSplitter import SuperpixelSplitter
from Algorithms.HooksGenerators.BezierHookGenerator import BezierHooksGenerator
from Algorithms.HooksGenerators.RectHookGenerator import RectHooksGenerator
from Algorithms.HooksGenerators.CrystalHookGenerator import CrystalHookGenerator
from Algorithms.HooksGenerators.HooksGenerator import HooksGenerator
import streamlit as st
import io


def get_splitter():
    splitters = {
        "Rectangular Splitter": RectSplitter(),
        "Hexagonal Splitter": HexSplitter(),
        "Voronoi Diagrams Splitter": VoronoiSplitter(),
        "Superpixels Splitter": SuperpixelSplitter()
    }
    return splitters[st.session_state["splitter_text"]]


def get_hooks_generator():
    generators = {
        "Bezier Hooks Generator (Usual round hooks)": BezierHooksGenerator(),
        "Rectangular Hooks Generator": RectHooksGenerator(),
        "Crystal Hooks Generator": CrystalHookGenerator(),
        "none": None
    }
    return generators[st.session_state["hooks_generator_text"]]


def process():
    img = Image.open(st.session_state["user_image"])
    white_img = create_white_image(img.size[0], img.size[1])
    splitter = get_splitter()
    generator = (PuzzleGenerator(img)
                 .set_splitter(splitter)
                 .generate_splitting(tile_h=st.session_state["tile_h"] if st.session_state.get("tile_h") else 0,
                                     tile_w=st.session_state["tile_w"] if st.session_state.get("tile_w") else 0,
                                     edge_size=st.session_state["edge_size"] if st.session_state.get(
                                         "edge_size") else 0,
                                     perfect_tiling=st.session_state["pure_hex"] if st.session_state.get(
                                         "pure_hex") is not None else True,
                                     num_tiles=st.session_state["vor_tiles"] if st.session_state.get(
                                         "vor_tiles") else 0,
                                     lloyds_iter=st.session_state["lloyds_iter"] if st.session_state.get(
                                         "lloyds_iter") else 0,
                                     num_superpixels=st.session_state["superpixel_regions"] if st.session_state.get(
                                         "superpixel_regions") else 0))
    hooks_generator: HooksGenerator = get_hooks_generator()
    if hooks_generator != None:
        generator = generator.set_hooks_generator(hooks_generator)
        if hooks_generator.name == "Rect Hooks Generator":
            hooks_base = st.session_state["rect_hook_base_point"] if st.session_state.get(
                "rect_hook_base_point") else 0.2
            first_seg_h = st.session_state["rect_first_seg_h"] if st.session_state.get("rect_first_seg_h") else 0.2
            second_seg_h = st.session_state["rect_second_seg_h"] if st.session_state.get("rect_second_seg_h") else 0.2
            wings_dist = st.session_state["rect_wings_dist"] if st.session_state.get("rect_wings_dist") else 0.15
            same_wings = st.session_state["rect_same_wings"] if st.session_state.get("rect_same_wings") else True
            drop_holds = st.session_state["rect_drop_holds"] if st.session_state.get("rect_drop_holds") else 0.0
            generator = generator.generate_hooks(hooks_base=hooks_base,
                                                 first_h=first_seg_h,
                                                 second_h=second_seg_h,
                                                 wings_dist=wings_dist,
                                                 same_wings=same_wings,
                                                 drop_holds=drop_holds)
        elif hooks_generator.name == "Crystal Hooks Generator":
            hooks_base = st.session_state["crystal_hook_base_point"] if st.session_state.get(
                "crystal_hook_base_point") else 0.2
            first_seg_h = st.session_state["crystal_first_seg_h"] if st.session_state.get(
                "crystal_first_seg_h") else 0.2
            second_seg_h = st.session_state["crystal_second_seg_h"] if st.session_state.get(
                "crystal_second_seg_h") else 0.2
            wings_dist = st.session_state["crystal_wings_dist"] if st.session_state.get("crystal_wings_dist") else 0.15
            same_wings = st.session_state["crystal_same_wings"] if st.session_state.get("crystal_same_wings") else True
            drop_holds = st.session_state["crystal_drop_holds"] if st.session_state.get("crystal_drop_holds") else 0.0
            generator = generator.generate_hooks(hooks_base=hooks_base,
                                                 first_h=first_seg_h,
                                                 second_h=second_seg_h,
                                                 wings_dist=wings_dist,
                                                 same_wings=same_wings,
                                                 drop_holds=drop_holds)
        elif hooks_generator.name == "Bezier Hooks Generator":
            hook_base_point = st.session_state["bezier_hook_base_point"] if st.session_state.get(
                "bezier_hook_base_point") else 0.0
            side_control_points_range = st.session_state["bezier_base_control_points"] if st.session_state.get(
                "bezier_base_control_points") else 0.0
            hook_wideness_range = st.session_state["bezier_top_control_points"] if st.session_state.get(
                "bezier_top_control_points") else 0.0
            generator = generator.generate_hooks(hook_base_point=hook_base_point,
                                                 side_control_points_range=side_control_points_range,
                                                 hook_wideness_range=hook_wideness_range)
    if st.session_state.get("shapes_uploader"):
        generator = generator.embedd_shapes(st.session_state["shapes_uploader"])
    generator = generator.draw_splitting()
    st.session_state["image"] = img
    generator.set_image(white_img)
    generator = generator.draw_splitting()
    st.session_state["white_img"] = white_img


st.set_page_config(layout="wide")
st.title("Procedural Puzzle Generator")
col1, col2 = st.columns(2)
with col2:
    st.header("Puzzle Preview")
    if st.session_state.get("user_image"):
        if not st.session_state.get("image"):
            st.session_state["image"] = Image.open(st.session_state.get("user_image"))
        st.image(st.session_state["image"])
        st.button("Generate Puzzle",
                  use_container_width=True,
                  on_click=process)
    image = st.file_uploader("Upload your image to be split",
                             type=["png", "jpg", "jpeg"],
                             key="user_image")

    if st.session_state.get("image"):
        output = io.BytesIO()
        st.session_state.get("image").save(output, format='PNG')
        st.download_button("Download splitting",
                           data=output.getvalue(), mime="image/png")
        output1 = io.BytesIO()
    if st.session_state.get("white_img"):
        st.session_state.get("white_img").save(output1, format='PNG')
        st.download_button("Download splitting on white background",
                           data=output1.getvalue(), mime="image/png")
    if image:
        st.session_state["image"] = Image.open(image)



def rect_splitter_options():
    img_size = st.session_state["image"].size
    st.number_input("Enter width of the tile",
                    min_value=int(img_size[0] / 30),
                    max_value=int(img_size[0] / 2),
                    step=1,
                    value=st.session_state["tile_w"] if st.session_state.get("tile_w") else int(img_size[0] / 10),
                    key="tile_w")
    st.number_input("Enter height of the tile",
                    min_value=int(img_size[1] / 30),
                    max_value=int(img_size[1] / 2),
                    value=st.session_state["tile_h"] if st.session_state.get("tile_h") else int(img_size[1] / 10),
                    step=1,
                    key="tile_h")


def voronoi_splitter_options():
    st.slider("Number of tiles",
              min_value=10,
              max_value=500,
              step=1,
              value=20,
              key="vor_tiles",
              )
    st.slider("Lloyds relaxation iterations",
              min_value=1, max_value=30,
              key="lloyds_iter",
              )


def hex_splitter_options():
    st.checkbox("Create pure hexagonal tiling? (alternative - shifted tiling with rombus.)",
                value=True,
                key="pure_hex",
                )
    img_size = st.session_state["image"].size
    st.number_input("enter length of the edge",
                    min_value=int(img_size[0] / 30),
                    max_value=int(img_size[0] / 4),
                    value=st.session_state["edge_size"] if st.session_state.get("edge_size") else int(
                        img_size[0] / 10) if int(img_size[0] / 10) % 2 == 0 else int(img_size[0] / 10) + 1,
                    step=2,
                    key="edge_size",
                    )


def superpixel_options():
    st.header("Warning: no hooks can be generated with superpixels splitting yet.")
    st.slider("Select number of superpixel regions",
              min_value=6,
              max_value=100,
              value=30,
              step=1,
              key="superpixel_regions",
              )


def bezier_generator_options():
    st.slider("Hook base point",
              min_value=0.1, max_value=0.4,
              step=0.01, value=0.3, key="bezier_hook_base_point",
              )
    st.slider("Base control points range (hook incut)",
              min_value=0.2, max_value=0.4,
              value=0.35, key="bezier_base_control_points")
    st.slider("Top control points range (hook wideness)",
              min_value=0.35, max_value=0.75,
              value=0.45, key="bezier_top_control_points")


def rect_generator_options():
    st.slider("Hook base point",
              min_value=0.1, max_value=0.4,
              step=0.01, key="rect_hook_base_point",
              )
    st.slider("First segment height",
              min_value=0.05, max_value=0.4,
              step=0.01, key="rect_first_seg_h",
              )
    st.slider("Second segment height",
              min_value=0.05, max_value=0.4,
              step=0.01, key="rect_second_seg_h",
              )
    st.slider("Wings distance",
              min_value=0.05, max_value=0.4,
              step=0.01, key="rect_wings_dist",
              )
    st.checkbox("Make hook symmetrical?",
                key="rect_same_wings",
                )
    st.slider("Drop some hooks? (enter fraction to drop)",
              min_value=0., max_value=0.4, step=0.01, key="rect_drop_holds",
              )


def crystal_generator_options():
    st.slider("Hook base point",
              min_value=0.1, max_value=0.4,
              step=0.01, key="crystal_hook_base_point",
              )
    st.slider("First segment height",
              min_value=0.05, max_value=0.5,
              step=0.01, key="crystal_first_seg_h",
              )
    st.slider("Second segment height",
              min_value=0.05, max_value=0.5,
              step=0.01, key="crystal_second_seg_h",
              )
    st.slider("Wings distance",
              min_value=0.05, max_value=0.5,
              step=0.01, key="crystal_wings_dist",
              )
    st.checkbox("Make hook symmetrical?",
                key="crystal_same_wings",
                )
    st.slider("Drop some hooks? (enter fraction to drop)",
              min_value=0., max_value=0.4, step=0.01, key="crystal_drop_holds")


with col1:
    st.header("Puzzle configuration")
    if not st.session_state.get("user_image"):
        st.header("Please upload your image to be split")
    else:
        sec1 = st.expander("Tiles Splitter Configuration")
        sec2 = st.expander("Hooks Generator Configuration")
        sec3 = st.expander("Additional Features Configuration")
        sec4 = st.expander("Post Processing Configuration")

        with sec1:
            st.subheader("Configure Tiles Splitter")
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Available Tiles Splitters",
                             options=[
                                 "Rectangular Splitter",
                                 "Hexagonal Splitter",
                                 "Voronoi Diagrams Splitter",
                                 "Superpixels Splitter"
                             ], key="splitter_text")
            with c2:
                if st.session_state.splitter_text == "Rectangular Splitter":
                    rect_splitter_options()
                elif st.session_state.splitter_text == "Hexagonal Splitter":
                    hex_splitter_options()
                elif st.session_state.splitter_text == "Voronoi Diagrams Splitter":
                    voronoi_splitter_options()
                elif st.session_state.splitter_text == "Superpixels Splitter":
                    superpixel_options()
        with sec2:
            st.subheader("Configure Hooks Generators")
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Available Hooks Generators",
                             options=[
                                 "Bezier Hooks Generator (Usual round hooks)",
                                 "Rectangular Hooks Generator",
                                 "Crystal Hooks Generator",
                                 "none"
                             ],
                             key="hooks_generator_text"
                             )
            with c2:
                if st.session_state.hooks_generator_text == "Bezier Hooks Generator (Usual round hooks)":
                    bezier_generator_options()
                elif st.session_state.hooks_generator_text == "Rectangular Hooks Generator":
                    rect_generator_options()
                elif st.session_state.hooks_generator_text == "Crystal Hooks Generator":
                    crystal_generator_options()
        with sec3:
            st.subheader("Additional Features Configuration")
            st.file_uploader("Upload PNG files containing ONLY outline of the shape (examples: https://drive.google.com/drive/folders/1jFucKoazClIDar9qK5ougBQHWbGH1nlz?usp=sharing)",
                             type="png", accept_multiple_files=True, key="shapes_uploader")

        with sec4:
            st.subheader("Configure Post Processing")
            st.subheader("Hooks intersection checking, and Boundaries checking are not yet available")

def create_white_image(x, y):
    data = np.ones((y, x, 3), dtype=np.uint8) * 255
    img = Image.fromarray(data, 'RGB')

    return img
