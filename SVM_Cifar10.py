#encoding:utf-8
import numpy as np
from data_input import load_CIFAR10
from SVM import SVM
import matplotlib.pyplot as plt
def VisualizeImage(X_train,y_train):
    plt.rcParams['figure.figsize'] = (10.0, 8.0)  # set default size of plots
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'
    classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    num_classes=len(classes)
    samples_per_class=8
    for y,cls in enumerate(classes):
        idxs=np.flatnonzero(y_train==y)
        idxs=np.random.choice(idxs,samples_per_class,replace=False)
        for i,idx in enumerate(idxs):
            plt_idx=i*num_classes+y+1
            plt.subplot(samples_per_class,num_classes,plt_idx)
            plt.imshow(X_train[idx].astype('uint8'))
            plt.axis('off')
            if i==0:
                plt.title(cls)
    plt.show()
def Visualizeloss(loss_history):
    plt.plot(loss_history)
    plt.xlabel('iteration number')
    plt.ylabel('loss value')
    plt.show()
def pre_dataset():
    cifar10_dir='/Users/yaoyao771/Downloads/cifar-10-batches-py'
    X_train,y_train,X_test,y_test=load_CIFAR10(cifar10_dir)
    VisualizeImage(X_train,y_train)
    input('enter any key to cross-validation')

    num_train=49000
    num_val=1000
    sample_index=range(num_train,num_train+num_val)
    X_train=X_train[:num_train]
    y_train=y_train[:num_train]
    X_val=X_train[sample_index]
    y_val=y_train[sample_index]

    X_train.np.reshape(X_train,(X_train.shape[0],-1))
    X_test=np.reshape(X_test,(X_test.shape[0],-1))
    X_val=np.rehsape(X_val,(X_val.shape[0],-1))

    mean_image=np.mean(X_train,axis=0)
    X_train=X_train-mean_image
    X_test=X_test-mean_image
    X_val=X_val-mean_image

    X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
    X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))])
    X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))])

    return X_train, y_train, X_test, y_test, X_val, y_val
def auto_get_parameter(X_train,y_train,X_val,y_val):
    learning_rates=[1e-7,5e-5]
    regularization_strength=[5e4,1e5]
    best_parameter=None
    best_val=-1
    for i in learning_rates:
        for i in regularization_strength:
            svm=SVM()
            y_pred=svm.predict(X_train,y_train,j,1,200,1500,True)
            acc_val=np.mean(y_val==y_pred)
            if best_val<acc_val:
                best_val=acc_val
                best_parameter=(i,j)
    print('have been identified parameter Best validation accuracy achieved during cross-validation: %f' % best_val )
    return best_parameter
def get_svm_model(parameter, X, y):
    svm = SVM()
    loss_history = svm.train(X, y, parameter[1], 1, parameter[0], 200, 1500, True)
    Visualizeloss(loss_history)
    input('Enter any key to predict...')
    return svm


if __name__ == '__main__':
    # 对数据进行预处理，得到训练集，测试集，验证集
    X_train, y_train, X_test, y_test, X_val, y_val = pre_dataset()
    # 通过验证集自动化确定参数 learning_rate和reg
    best_parameter = auto_get_parameter(X_train, y_train, X_val, y_val)
    # 通过参数和训练集构建SVM模型
    svm = get_svm_model(best_parameter, X_train, y_train)
    # 用测试集预测准确率
    y_pred = svm.predict(X_test)
    print('Accuracy achieved during cross-validation: %f' % (np.mean(y_pred == y_test)))



