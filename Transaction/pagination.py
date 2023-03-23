# from rest_framework.pagination import PageNumberPagination
#
# class Add_TransactionPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'
#     max_page_size = 10000


from rest_framework.pagination import LimitOffsetPagination


class Add_TransactionPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000