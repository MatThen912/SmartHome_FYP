from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'smartpoultrydw' # Must be replaced by your <storage_account_name>
    account_key = 'pjT+gn576xfn1LIWVKYq5Ed4IrjrS7Fsk0ZE2u+QTNxtOmz3SQJ5pbgGozIDpmWxyA6YofdIP9xoLkl+FatM5w==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None


# class AzureStaticStorage(AzureStorage):
#     account_name = 'smartpoultrydw' # Must be replaced by your storage_account_name
#     account_key = 'pjT+gn576xfn1LIWVKYq5Ed4IrjrS7Fsk0ZE2u+QTNxtOmz3SQJ5pbgGozIDpmWxyA6YofdIP9xoLkl+FatM5w==' # Must be replaced by your <storage_account_key>
#     azure_container = 'static'
#     expiration_secs = None

