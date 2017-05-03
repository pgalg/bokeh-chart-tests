# makes standalone html


import pandas as pd
from bokeh.io import show
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import RadioGroup
from bokeh.models import CustomJS ,ColumnDataSource
from bokeh.plotting import figure, output_file

df = pd.read_excel('TPbars.xlsx')
baseline=df.iloc[0:1,0:4]
s1=df.iloc[1:2,0:4] # water saving
s2=df.iloc[2:3,0:4] # lw
s3=df.iloc[3:4,0:4] # water saving and lw

s1["Scenario"] = "Improved rose"
s2["Scenario"] = "Improved rose"
s3["Scenario"] = "Improved rose"

values = (baseline,s1,s2,s3)
#change social cost to social cost top (social cost + retail cost)
for i in values:
   i["Social cost"]=i["Social cost"]+i["Retail price"]
   i.rename(index=str, columns={"Social cost": "Social cost top"}, inplace = True)
#change env cost to env cost top (env cost + social cost top)
for i in values:
   i["Water cost"]=i["Water cost"]+i["Social cost top"]
   i.rename(index=str, columns={"Water cost": "Water cost top"}, inplace = True)

normal = ColumnDataSource(baseline)
normal1 = ColumnDataSource(s1)
improved1 = ColumnDataSource(s1)
improved2 = ColumnDataSource(s2)
improved3 = ColumnDataSource(s3)

#plots
plot = figure(
    plot_height=400,
    plot_width=600,
    x_range=["Normal rose","Improved rose"],
    y_range=(0, 20),
    title="Price of a Kenyan rose",
    tools="",
    logo="grey")

bluenormalbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Retail price",
    color="MidnightBlue",
    legend="Market price",
    visible=True,
    source=normal
    )
blueimprovedbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Retail price",
    color="MidnightBlue",
    legend="Market price",
    visible=True,
    source=normal1
    )

rednormalbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Social cost top",
    bottom="Retail price",
    color = "FireBrick",
    legend="Social cost",
    source=normal
    )

redimprovedbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Social cost top",
    bottom="Retail price",
    color = "FireBrick",
    legend="Social cost",
    source=normal1
)
greennormalbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Water cost top",
    bottom="Social cost top",
    color="SeaGreen",
    legend="Water cost",
    visible=True,
    source=normal
    )
greenimprovedbar= plot.vbar(
    x="Scenario",
    width=0.5,
    top="Water cost top",
    bottom="Social cost top",
    color="SeaGreen",
    legend="Water cost",
    visible=True,
    source=normal1
    )


#this changes the source data of blueimproved, back and forth,
callback = CustomJS(args=(dict(improved=blueimprovedbar, s1=improved1, s2=improved2, s3=improved3)), code="""
    var source = improved.data_source;

    if (cb_obj.active == 0) {
        source.data = s1.data
    } else if (cb_obj.active == 1) {
        source.data = s2.data
    } else if (cb_obj.active == 2) {
        source.data = s3.data
    }
    improved.trigger('change');
    """)

widgets = RadioGroup(
    labels=["Water saving", "Living wage","Water saving + Living wage"], 
    callback=callback,
    active=0,
    width=600
)

layout=(column(plot,widgetbox(widgets), sizing_mode="scale_width"))

plot.title.text_font = "Bitter"
plot.legend.label_text_font = 'open sans'
plot.axis.axis_label_text_font = 'open sans'
plot.yaxis.axis_label = "USD/bouquet"
plot.axis.major_label_text_font = 'open sans'

output_file("widgets.html")

show(layout)



