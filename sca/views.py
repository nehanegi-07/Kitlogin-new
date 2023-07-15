from django.views.generic import View
from django.shortcuts import render
from sca.datapipe.pipeline import Pipeline
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from datetime import datetime
import os.path
import json



@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'success': True})



@method_decorator(csrf_exempt, name='dispatch')
class ScaView(View):    
    def post(self, request):
        print("in post")
        data = json.loads(request.body.decode('utf-8'))
        
        # pipeline = Pipeline(request.POST.get('time_stamp'), request.POST.get('owner_address'), request.POST.get('contract_address'))
        # pipeline.start(force_get=True)
        # return render(request, 'success.html')")
        timestamp = time.time()
        dt_object = datetime.fromtimestamp(timestamp)
        comp_name = dt_object.strftime("%Y-%m-%d_%H-%M-%S")
        hex_address = data.get('hex_address')
        path = f"{os.getcwd()}/sca/resource/sca_config.ini"
        pipeline = Pipeline(comp_name, path, hex_address)

        json_dict = pipeline.start(force_get=True)
        
        return JsonResponse(json_dict)

