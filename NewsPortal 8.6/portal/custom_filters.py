from django import template

register = template.Library()

censor_list = ['стал', 'лучшим', 'фонд', 'рынка']


@register.filter()
def censor(value):

   value1 = ''
   if isinstance(value, str):
      for i in value.split():
         if i and i.lower() in censor_list:
            i = i.replace(i[1:], '*' * (len(i) - 1))
         value1 = value1 + ' ' + i
   else:
      raise TypeError("Несоответствие типа данных")
   return f'{value1}'
