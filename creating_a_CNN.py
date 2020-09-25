import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

(train_images, train_labels),(test_images, test_lables) = datasets.cifar10.load_data()

train_images, test_images = train_images/255.0, test_images/255.0
class_names = ['airplane', 'automobiles', 'bird', 'cat','deer', 'dog', 'frog', 'horse', 'ship', 'truck']
IMG_INDEX  = 1
plt.imshow(train_images[IMG_INDEX], cmap=plt.cm.binary)
plt.xlabel(class_names[train_labels[IMG_INDEX][0]])
#plt.show()
model = models.Sequential()
model.add(layers.Conv2D(32,(3,3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D(2, 2))
model.add(layers.Conv2D(64,(3,3), activation='relu'))
#model.summary()
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))
#model.summary()
model.compile(optimizer='adam',
loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
metrics=['accuracy'])
history = model.fit(train_images,train_labels, epochs=1, validation_data=(test_images, test_lables))
test_loss, test_acc = model.evaluate(test_images, test_lables, verbose = 2)