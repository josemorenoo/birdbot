BASE_PATH = "assets/file_extension_imgs/"

FILE_EXTENSIONS = {
    "c": {"path": BASE_PATH + "c.png", "classification": "backend"},
    "css": {"path": BASE_PATH + "css.png", "classification": "frontend"},
    "csv": {"path": BASE_PATH + "csv.png", "classification": "config"},
    "cjs": {"path": BASE_PATH + "commonjs.png", "classification": "frontend"},
    "d": {"path": BASE_PATH + "d.png", "classification": "backend"},
    "dockerfile": {"path": BASE_PATH + "docker.png", "classification": "config"},
    "docker-build": {"path": BASE_PATH + "docker.png", "classification": "config"},
    "dune": {"path": BASE_PATH + "dune.png", "classification": "backend"},
    "go": {"path": BASE_PATH + "golang.png", "classification": "backend"},
    "h": {"path": BASE_PATH + "c.png", "classification": "backend"},
    "html": {"path": BASE_PATH + "html.png", "classification": "frontend"},
    "kt": {"path": BASE_PATH + "kt.png", "classification": "mobile"},
    "js": {"path": BASE_PATH + "js.png", "classification": "frontend"},
    "jsx": {"path": BASE_PATH + "react.png", "classification": "frontend"},
    "json": {"path": BASE_PATH + "json.png", "classification": "config"},
    "jpg": {"path": BASE_PATH + "image.png", "classification": "config"},
    "md": {"path": BASE_PATH + "md.png", "classification": "docs"},
    "mdx": {"path": BASE_PATH + "md.png", "classification": "docs"},
    "ml": {"path": BASE_PATH + "ml.png", "classification": "backend"},
    "ocaml": {"path": BASE_PATH + "ocaml.png", "classification": "backend"},
    "pdf": {"path": BASE_PATH + "pdf.png", "classification": "docs"},
    "png": {"path": BASE_PATH + "image.png", "classification": "docs"},
    "proto": {"path": BASE_PATH + "proto.png", "classification": "config"},
    "pbxproj": {"path": BASE_PATH + "xcode.png", "classification": "backend"},
    "py": {"path": BASE_PATH + "py.png", "classification": "backend"},
    "rs": {"path": BASE_PATH + "rs.png", "classification": "backend"},
    "scss": {"path": BASE_PATH + "css.png", "classification": "frontend"},
    "sh": {"path": BASE_PATH + "sh.png", "classification": "backend"},
    "swift": {"path": BASE_PATH + "swift.png", "classification": "mobile"},
    "svelte": {"path": BASE_PATH + "svelte.png", "classification": "frontend"},
    "txt": {"path": BASE_PATH + "txt.png", "classification": "docs"},
    "tf": {"path": BASE_PATH + "tf.png", "classification": "config"},
    "toml": {"path": BASE_PATH + "toml.png", "classification": "config"},
    "ts": {"path": BASE_PATH + "ts.png", "classification": "frontend"},
    "tsx": {"path": BASE_PATH + "ts.png", "classification": "frontend"},
    "vue": {"path": BASE_PATH + "vue.png", "classification": "frontend"},
    "yml": {"path": BASE_PATH + "yaml.png", "classification": "config"},
    "yaml": {"path": BASE_PATH + "yaml.png", "classification": "config"},
}

import boto3


def download_s3_file(
    filename,
    bucket_name="coincommit",
    key="assets/twitter_logos/",
):
    filename += ".png"
    local_file_path = BASE_PATH + filename
    key += filename

    s3 = boto3.client("s3")
    try:
        s3.download_file(bucket_name, key, local_file_path)
        print(f"File downloaded from s3://{bucket_name}/{key} to {local_file_path}")
    except Exception as e:
        print(f"Error downloading file from s3://{bucket_name}/{key}: {e}")
