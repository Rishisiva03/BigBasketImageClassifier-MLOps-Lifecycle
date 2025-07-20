import sys
import os
import json
import streamlit as st
import mlflow
import mlflow.pyfunc
from PIL import Image
import torch
import torchvision.transforms as transforms

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.config import LABEL_MAP_PATH


@st.cache_resource
def get_registered_models():
    client = mlflow.MlflowClient()
    return [rm.name for rm in client.search_registered_models()]

@st.cache_resource
def get_model_versions(name):
    client = mlflow.MlflowClient()
    versions = client.get_latest_versions(name)
    return {f"v{v.version} ({v.current_stage})": v.version for v in versions}

@st.cache_resource
def load_model(name, version):
    model_uri = f"models:/{name}/{version}"
    print(f"Loading model from URI: {model_uri}")
    return mlflow.pyfunc.load_model(model_uri)

@st.cache_resource
def load_label_map(model_name, label_path = LABEL_MAP_PATH):
    
    if model_name == "bb_classifier_subcategory":
        label_path = label_path.replace("label_map_category.json", "label_map.json")
        print(label_path)
    with open(label_path, "r") as f:
        label_map = json.load(f)
    return {v: k for k, v in label_map.items()}


def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ])
    if image.mode != 'RGB':
        image = image.convert("RGB")
    return transform(image).unsqueeze(0)

st.set_page_config(page_title="Grocery Classifier", layout="centered")
st.title("Grocery Classifier Inference with MLflow")


registered_models = get_registered_models()

if not registered_models:
    st.error("No registered models found in MLflow Registry.")
    st.stop()

model_name = st.selectbox("Choose a Registered Model", registered_models)

model_versions = get_model_versions(model_name)
if not model_versions:
    st.error(f"No versions found for model '{model_name}'.")
    st.stop()

version_label = st.selectbox("Choose Model Version", list(model_versions.keys()))
selected_version = model_versions[version_label]

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])
image_path = st.text_input("Or enter a local image file path")

if uploaded_file or image_path:
    try:
        if uploaded_file:
            image = Image.open(uploaded_file)
        else:
            if not os.path.exists(image_path):
                st.error("Invalid file path.")
                st.stop()
            image = Image.open(image_path)

        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Predicting..."):
            model = load_model(model_name, selected_version)
            label_map = load_label_map(model_name)
            st.write(label_map.values())
            input_tensor = preprocess_image(image)

            with torch.no_grad():
                preds = model.predict(input_tensor.numpy())
                pred_class = int(preds.argmax())

            predicted_label = label_map[pred_class]
            st.success(f"Predicted Category: **{predicted_label}**")

    except Exception as e:
        st.error(f"Error during prediction: {e}")
