from django.urls import path
from .view import ProudctList
from .view import ProductAdd
from .view import ProductEdit
from .view import ProductEditPhoto
from .view import SeeOrEditToLabelAndDetails

urlpatterns = [
    path(r'ProductList', ProudctList.index),
    path(r'ProductList/GetProductList/', ProudctList.GetProductList),
    path(r'ProductList/ExcelAdd/', ProudctList.ExcelAdd),
    path(r'ProductList/Del/', ProudctList.Del),

    path(r'ProductAdd', ProductAdd.index),
    path(r'ProductAdd/Add/', ProductAdd.Add),

    path(r'ProductEdit', ProductEdit.index),
    path(r'ProductEdit/Edit/', ProductEdit.Edit),

    path(r'ProductEditPhoto', ProductEditPhoto.index),
    path(r'ProductEditPhoto/ImgUpload/', ProductEditPhoto.ImgUpload),

    path(r'SeeOrEditToLabelAndDetails', SeeOrEditToLabelAndDetails.index),
    path(r'SeeOrEditToLabelAndDetails/Edit/', SeeOrEditToLabelAndDetails.Edit)
]
