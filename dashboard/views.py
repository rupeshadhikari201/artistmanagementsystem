import logging
from django.contrib import messages
from django.shortcuts import render 

from core.decorators import login_required
from .queries import get_dashboard_stats

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    
    user = request.session.get('user')
    
    try:
        stats = get_dashboard_stats()
    except Exception:
        messages.error(request, 'Error Fetching dashboard stats')
        logger.exception('dashboard stats failed')
        stats = {}

    return render(
        request, 
        'dashboard/dashboard.html', 
        {
            'user':  user,
            'stats': stats,
        }
    )