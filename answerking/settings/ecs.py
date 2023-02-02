"""
ECS settings for answerking project.
"""
from answerking.settings.base import *
from answerking_app.utils.get_ecs_ips import get_ecs_task_ips

# Add ip(s) to ALLOWED HOSTS django setting
ALLOWED_HOSTS += get_ecs_task_ips()
