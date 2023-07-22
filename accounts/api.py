from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
import pandas as pd

import pandas as pd
# For Charting Purposes
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from django.db import transaction
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from accounts.decorators import login_exempt
from django.views.decorators.cache import cache_page


