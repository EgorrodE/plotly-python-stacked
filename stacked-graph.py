import plotly.plotly as py
import plotly.graph_objs as go
import datetime as dt
import random as rand
import string

rand_x = []
rand_y = {'1 bad': [], '1 norm': [], '2 bad': [], '2 norm': [], '3 bad': [], '3 norm': [], '4 bad': [], '4 norm': []}
texts = {'1 bad': [], '1 norm': [], '2 bad': [], '2 norm': [], '3 bad': [], '3 norm': [], '4 bad': [], '4 norm': []}
bad_template = string.Template("$num bad")
norm_template = string.Template("$num norm")
colors = {
  '1 bad':  '#ff3d3d',
  '1 norm': '#ff8a8a',
  '2 bad':  '#ff8d20',
  '2 norm': '#ffb269',
  '3 bad':  '#fffe00',
  '3 norm': '#fffe71',
  '4 bad':  '#41ff43',
  '4 norm': '#90fa91'
}
maxes = [0.3, 0.6, 0.8]
traces = []
layout = go.Layout(
  showlegend=True,
  xaxis=dict(
    type='category'
  ),
  yaxis=dict(
    type='linear',
    range=[0, 1],
    dtick=0.2
  ),
  width=1000,
  height=1000,
  plot_bgcolor='#c7c7c7'
)

def generate_x_values():
  tmp = dt.date(2014, 3, 1)
  for i in range(12):
    rand_x.append(tmp)
    if tmp.month == 12:
      tmp = tmp.replace(year = tmp.year + 1, month = 3)
    else:
      tmp = tmp.replace(month = tmp.month + 3)

def generate_y_values():
  for i in range(12):
    bottom = 0
    top = 1
    for j in range(1,4):
      tmp = rand.uniform(bottom, maxes[j - 1])
      tmp2 = rand.uniform(bottom, bottom + (tmp - bottom) / (j + 1))
      rand_y[bad_template.substitute(num = j)].append(tmp2)
      rand_y[norm_template.substitute(num = j)].append(tmp)
      texts[norm_template.substitute(num = j)].append(str(tmp - bottom))
      texts[bad_template.substitute(num = j)].append(f"{((tmp2 - bottom) * 100 / (tmp - bottom)):.2f}" + '%')
      bottom = tmp
    tmp = rand.uniform(bottom, bottom + (top - bottom) / 5)
    rand_y[bad_template.substitute(num = 4)].append(tmp)
    rand_y[norm_template.substitute(num = 4)].append(top)
    texts[norm_template.substitute(num = 4)].append(str(top - bottom))
    texts[bad_template.substitute(num = 4)].append(f"{((tmp - bottom) * 100 / (top - bottom)):.2f}" + '%')

def create_trace(name):
  trace_name = 'class: ' + name[0]
  if 'bad' in name:
    trace_name += '(bad)'
  return go.Scatter(
    x=rand_x,
    y=rand_y[name],
    name=trace_name,
    mode='lines',
    line=dict(
      width=0.5,
      color=colors[name]),
    text=texts[name],
    hoverinfo='name+text',
    fill='tonexty'
  )

def perform():
  generate_x_values()
  generate_y_values()
  for i in range(1,5):
    traces.append(create_trace(bad_template.substitute(num=i)))
    traces.append(create_trace(norm_template.substitute(num=i)))
  fig = go.Figure(data=traces, layout=layout)
  py.iplot(fig, filename='stacked-area-plot')

perform()
