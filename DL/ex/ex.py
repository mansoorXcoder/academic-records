"""
exp1_mlp_mnist_images.py
MLP on MNIST when dataset is saved as image files.
Supports two formats: 'dir' (preferred) and 'flat' (label in filename).
Run: python exp1_mlp_mnist_images.py
"""

import os
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import random

# --------- USER CONFIG ----------
DATA_ROOT = Path(r"D:\LE03\DL\Exp 1\Datasets")  # your folder (will try common fallbacks)
DATA_FORMAT = "dir"   # "dir" or "flat"
TRAIN_DIR = DATA_ROOT / "train"   # used when DATA_FORMAT == "dir"
TEST_DIR  = DATA_ROOT / "test"    # used when DATA_FORMAT == "dir"
FLAT_DIR  = DATA_ROOT / "all_images"  # used when DATA_FORMAT == "flat" or fallback
IMAGE_SIZE = (28, 28)
BATCH_SIZE = 256
EPOCHS = 12
MODEL_SAVE = Path("mlp_mnist_images_model.h5")
RANDOM_SEED = 42
# --------------------------------

tf.random.set_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


def is_image_file(p: Path):
    return p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.bmp')


def load_from_directory(train_dir, test_dir, image_size, batch_size):
    print(f"Loading from directory structure (train/<label>/* , test/<label>/*)...")
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        str(train_dir),
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=batch_size,
        image_size=image_size,
        shuffle=True,
        seed=RANDOM_SEED
    )
    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        str(test_dir),
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=batch_size,
        image_size=image_size,
        shuffle=False
    )
    return train_ds, test_ds


def load_from_flat(flat_dir, image_size):
    print("Loading from flat folder with filenames 'label_xxx.ext' ...")
    images = []
    labels = []
    pth = Path(flat_dir)
    if not pth.exists():
        raise SystemExit(f"Flat-folder not found: {pth}")
    for p in sorted(pth.glob("*")):
        if not is_image_file(p):
            continue
        name = p.stem  # filename without ext
        # expect label_... or label-... or single digit name
        label = None
        if "_" in name:
            label = name.split("_")[0]
        elif "-" in name:
            label = name.split("-")[0]
        else:
            label = name  # if file is like '7' or '0'
        try:
            lbl = int(label)
        except:
            print(f"Skipping file with non-integer label: {p.name}")
            continue
        img = tf.io.read_file(str(p))
        img = tf.image.decode_image(img, channels=1)
        img = tf.image.resize(img, image_size)
        img = tf.cast(img, tf.float32) / 255.0
        images.append(img.numpy().reshape(-1))  # flatten
        labels.append(lbl)
    if len(images) == 0:
        raise SystemExit("No images found in flat folder.")
    X = np.stack(images, axis=0)
    y = np.array(labels, dtype=np.int32)
    # simple 90/10 split
    split = int(0.9 * len(X))
    idx = np.random.RandomState(RANDOM_SEED).permutation(len(X))
    X = X[idx]
    y = y[idx]
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    return (X_train, y_train), (X_test, y_test)


def load_from_label_folders(root_dir, image_size, test_ratio=0.2):
    """
    root_dir contains subfolders for each label: root/0/*, root/1/* ...
    We'll read images per label and create an in-memory train/test split.
    """
    print(f"Loading from labeled folders inside: {root_dir} (will split per-label {int((1-test_ratio)*100)}/{int(test_ratio*100)})")
    root = Path(root_dir)
    labels_dirs = [d for d in sorted(root.iterdir()) if d.is_dir()]
    if not labels_dirs:
        raise SystemExit(f"No label subfolders found in {root_dir}")
    X_train_list, y_train_list, X_test_list, y_test_list = [], [], [], []
    for lbl_dir in labels_dirs:
        label_name = lbl_dir.name
        try:
            label = int(label_name)
        except:
            print(f"Skipping non-int label folder: {label_name}")
            continue
        files = [p for p in sorted(lbl_dir.glob("*")) if is_image_file(p)]
        if not files:
            print(f"Warning: no images found in folder {lbl_dir}")
            continue
        # shuffle files and split
        rng = np.random.RandomState(RANDOM_SEED)
        idx = rng.permutation(len(files))
        split = int((1 - test_ratio) * len(files))
        train_idx = idx[:split]
        test_idx = idx[split:]
        def read_list(ix_list):
            imgs = []
            for i in ix_list:
                p = files[i]
                img = tf.io.read_file(str(p))
                img = tf.image.decode_image(img, channels=1)
                img = tf.image.resize(img, image_size)
                img = tf.cast(img, tf.float32) / 255.0
                imgs.append(img.numpy().reshape(-1))
            return np.stack(imgs, axis=0)
        X_tr = read_list(train_idx)
        X_te = read_list(test_idx) if len(test_idx) > 0 else np.empty((0, image_size[0]*image_size[1]))
        y_tr = np.full((X_tr.shape[0],), label, dtype=np.int32)
        y_te = np.full((X_te.shape[0],), label, dtype=np.int32)
        X_train_list.append(X_tr); y_train_list.append(y_tr)
        if X_te.shape[0] > 0:
            X_test_list.append(X_te); y_test_list.append(y_te)
    if not X_train_list:
        raise SystemExit("No training data collected from labeled folders.")
    X_train = np.concatenate(X_train_list, axis=0)
    y_train = np.concatenate(y_train_list, axis=0)
    if X_test_list:
        X_test = np.concatenate(X_test_list, axis=0)
        y_test = np.concatenate(y_test_list, axis=0)
    else:
        # if no test images created (small dataset), split from training
        idx = np.random.RandomState(RANDOM_SEED).permutation(len(X_train))
        split = int(0.9 * len(X_train))
        X_train = X_train[idx]; y_train = y_train[idx]
        X_test, y_test = X_train[split:], y_train[split:]
        X_train, y_train = X_train[:split], y_train[:split]
    return (X_train, y_train), (X_test, y_test)


def build_mlp(input_dim, num_classes=10):
    model = Sequential([
        Dense(256, activation='relu', input_shape=(input_dim,)),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def plot_history(history):
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(history.history['loss'], label='train_loss')
    if 'val_loss' in history.history: plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend(); plt.title("Loss")
    plt.subplot(1,2,2)
    plt.plot(history.history['accuracy'], label='train_acc')
    if 'val_accuracy' in history.history: plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.legend(); plt.title("Accuracy")
    plt.tight_layout(); plt.savefig("training_curves.png", dpi=150); plt.show()


def main():
    # Auto-detect / fallback logic
    print("DATA_ROOT:", DATA_ROOT)
    train_ds = test_ds = None
    X_train = X_test = y_train = y_test = None

    if DATA_FORMAT == "dir":
        # direct use if both train/test exist
        if TRAIN_DIR.exists() and TEST_DIR.exists():
            print("Found explicit TRAIN and TEST folders.")
            train_ds, test_ds = load_from_directory(TRAIN_DIR, TEST_DIR, IMAGE_SIZE, BATCH_SIZE)
        else:
            # try some common fallbacks
            alt_candidates = [
                DATA_ROOT / "Dataset",
                DATA_ROOT / "dataset",
                DATA_ROOT,  # maybe DATA_ROOT itself contains label folders
            ]
            found = False
            for candidate in alt_candidates:
                if candidate.exists():
                    # if candidate has train/test subfolders
                    if (candidate / "train").exists() and (candidate / "test").exists():
                        TRAIN_DIR = candidate / "train"
                        TEST_DIR = candidate / "test"
                        print(f"Using fallback train/test: {TRAIN_DIR}, {TEST_DIR}")
                        train_ds, test_ds = load_from_directory(TRAIN_DIR, TEST_DIR, IMAGE_SIZE, BATCH_SIZE)
                        found = True
                        break
                    # if candidate contains label subfolders, we'll load & split in-memory
                    label_subdirs = [d for d in candidate.iterdir() if d.is_dir()]
                    if label_subdirs:
                        print(f"Found labeled subfolders in {candidate}. Will load & split per-label.")
                        (X_train, y_train), (X_test, y_test) = load_from_label_folders(candidate, IMAGE_SIZE, test_ratio=0.2)
                        found = True
                        break
            if not found:
                raise SystemExit(f"Train/test folders not found. Expected {TRAIN_DIR} and {TEST_DIR}, and fallbacks failed.")

        # if we got tf.data datasets, convert to numpy arrays
        if train_ds is not None and test_ds is not None:
            def ds_to_numpy(ds):
                xs = []
                ys = []
                # iterate without batching interference
                for batch_x, batch_y in ds.unbatch().batch(1024):
                    xs.append(batch_x.numpy())
                    ys.append(batch_y.numpy())
                X = np.concatenate(xs, axis=0)
                y = np.concatenate(ys, axis=0)
                # from shape (N, H, W, 1) -> (N, H*W)
                X = X.reshape(X.shape[0], -1)
                return X, y
            X_train, y_train = ds_to_numpy(train_ds)
            X_test, y_test = ds_to_numpy(test_ds)

    elif DATA_FORMAT == "flat":
        # If flat dir explicitly provided, use it; otherwise try common names
        if Path(FLAT_DIR).exists():
            (X_train, y_train), (X_test, y_test) = load_from_flat(FLAT_DIR, IMAGE_SIZE)
        else:
            alt_flat = [DATA_ROOT / "all_images", DATA_ROOT / "images", DATA_ROOT]
            found = False
            for f in alt_flat:
                if f.exists():
                    try:
                        (X_train, y_train), (X_test, y_test) = load_from_flat(f, IMAGE_SIZE)
                        found = True; break
                    except SystemExit:
                        continue
            if not found:
                raise SystemExit("Flat format selected but no suitable flat folder found.")
    else:
        raise SystemExit("Unknown DATA_FORMAT. Use 'dir' or 'flat'.")

    print("Shapes:", X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    # Ensure normalized (dir loader already normalized but check anyway)
    if X_train.max() > 1.0:
        X_train = X_train.astype(np.float32) / 255.0
        X_test  = X_test.astype(np.float32) / 255.0

    model = build_mlp(X_train.shape[1])
    model.summary()

    ckpt = ModelCheckpoint(str(MODEL_SAVE), monitor='val_accuracy', save_best_only=True, verbose=1)
    es = EarlyStopping(monitor='val_accuracy', patience=4, restore_best_weights=True, verbose=1)

    history = model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=EPOCHS,
        batch_size=128,
        callbacks=[ckpt, es],
        verbose=2
    )

    plot_history(history)

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test acc: {test_acc:.4f}")

    y_pred = np.argmax(model.predict(X_test), axis=1)
    print("\nClassification report:\n", classification_report(y_test, y_pred, digits=4))
    print("Confusion matrix shape:", confusion_matrix(y_test, y_pred).shape)

    model.save(MODEL_SAVE)
    print("Saved model:", MODEL_SAVE.resolve())


if __name__ == "__main__":
    main()
