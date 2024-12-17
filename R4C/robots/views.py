from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime as dt

@csrf_exempt
def add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            errors = validate(data)
            if errors:
                return JsonResponse({'errors': errors}, status=400)

            serial = data.get('serial')
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')


            response_data = {
                'status': 'success',
                'serial': serial,
                'model': model,
                'version': version,
                'created': created,
            }
            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def validate(data):
    errors = {}
    
    if ('serial' and 'model' and 'version' and 'created') not in data:
        errors['All'] = 'All information(serial, model, version and created) is required.'
    
    if len(data['serial']) != 5:
        errors['serial'] = 'Serial must be 5 characters long.'

    if len(data['model']) != 2 or len(data['version']) != 2:
        errors['model/version'] = 'Model and version must be 2 characters long each.'

    if not dt.strptime(data['created'], '%Y-%m-%d %H:%M:%S'):
        errors['created'] = 'Created must be in format - YYYY-MM-DD HH:MM:SSc.'

    return errors