from os.path import dirname, join
import os
import pandas as pd
import math
import datetime

from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import RangeSlider, Button, DataTable, TableColumn, NumberFormatter, CheckboxGroup, TextInput, Slider
from bokeh.io import curdoc
import queries

# find range of flow months
maxmin = queries.data_query(queries.maxmindate())
finalMonth = maxmin['maxdate'].iloc[0].month
finalYear = maxmin['maxdate'].iloc[0].year
firstMonth = maxmin['mindate'].iloc[0].month
firstYear = maxmin['mindate'].iloc[0].year


# get list of all TDSPs
tdsps = queries.data_query(queries.alltdsps()).values.flatten().tolist()

querygen = queries.monthlygen(flowdates=[str(finalYear) + '-' + str(finalMonth).rjust(2,'0') + '-01'],
                          TDSP=tdsps)

source = ColumnDataSource(data=dict())
source_dl = ColumnDataSource(data=dict())

def update():
    # print('updating.')
    # Get the current slider values
    filterMonth = int(month_slider.value)
    filterYear = int(year_slider.value)

    esiid = esiid_textbox.value.lower()

    exclude = exclude_approval_textbox.value.lower()

    # Filter on TDSP
    selected_TDSPs = [tdsps[x] for x in tdsp_group.active]

    # Filter on ESIID
    noesiid = (esiid == 'none') | (esiid == '')
    noexclude = (exclude == 'none') | (exclude == '')
    if noesiid or noexclude:
        querygen = queries.query_transactions(flowdates=[str(filterYear) + '-' + str(filterMonth).rjust(2,'0') + '-01'],
                                  TDSP=selected_TDSPs)
    elif noexclude and not noesiid:
        querygen = queries.query_transactions(flowdates=[str(filterYear) + '-' + str(filterMonth).rjust(2,'0') + '-01'],
                                  TDSP=selected_TDSPs,
                                  ESIID = [esiid])
    elif noesiid and not noexclude:
        querygen = queries.query_transactions(flowdates=[str(filterYear) + '-' + str(filterMonth).rjust(2,'0') + '-01'],
                                  TDSP=selected_TDSPs)
    else:
        querygen = query.query_transactions(flowdates = [str(filterYear) + '-' + str(filterMonth).rjust(2,'0') + '-01'],
                                  TDSP=selected_TDSPs,
                                  ESIID = [esiid])
    df = queries.data_query(querygen)


    # create a copy of the df for download purposes, manipulate it to make it more user friendly ($'s and rounding)
    df_dl = df.copy()
    df_dl.DocumentTrackingNumber = '="' + df_dl.DocumentTrackingNumber + '"'
    df_dl.OriginalDocumentID = '="' + df_dl.OriginalDocumentID + '"'
    df_dl.MarketerDUNS = '="' + df_dl.MarketerDUNS + '"'
    df_dl.ESIID = '="' + df_dl.ESIID + '"'
    df_dl.InvoiceTotalAmount = df_dl.InvoiceTotalAmount.apply(lambda x: '${:.2f}'.format(x))

    source.data = df.to_dict('list')
    source_dl.data = df_dl.to_dict('list')

# Set up widgets
esiid_textbox = TextInput(title='ESIID', value='None')


#day_slider = Slider(title='day', value=1, start=1, end=31, step=1)

month_slider = Slider(title='month', value=finalMonth, start=1, end=12, step=1)

year_slider = Slider(title='year', value=finalYear, start=firstYear, end=finalYear, step=1)

tdsp_group = CheckboxGroup(labels=tdsps,
                           active=list(range(len(tdsps))))

exclude_approval_textbox = TextInput(title='Exclude' value='None')

savebutton = Button(label="Download", button_type="success")
savebutton.callback = CustomJS(args=dict(source=source_dl), code=open(os.path.join(os.path.dirname(__file__), "dl_820transactions.js")).read())

#updatebutton = Button(label="Approve", button_type="")
#updatebutton.callback =


columns = [
    TableColumn(field="DocumentTrackingNumber", title="Document Tracking Number", width=150),
    TableColumn(field="OriginalDocumentID", title="Original Document ID", width=100),
    TableColumn(field="MarketerDUNS", title="Marketer DUNS", width=100),
    TableColumn(field="TDSP", title="TDSP", width=75),
    TableColumn(field="PaymentDueDate", title="Payment Due Date", width=100, formatter=DateFormatter(format="%m/%d/%Y")),
    TableColumn(field="ESIID", title="ESIID", width=100),
    TableColumn(field="InvoiceTotalAmount", title="Invoice Total Amount", width=100, formatter=NumberFormatter(format='$0,0.00')),
    TableColumn(field="Processed", title="Processed", width=75),
]

data_table = DataTable(source=source,
                       columns=columns,
                       width=800,
                       height = 400,
                       scroll_to_selection = False,
                       sortable = True,
                       fit_columns = False,
                       selectable=True,
                       row_headers=False)

controls1 = widgetbox(esiid_textbox)
controls2 = widgetbox(#day_slider,
					  month_slider,
                      year_slider)
controls3 = widgetbox(tdsp_group,exclude_approval_textbox)
table = widgetbox(data_table)

curdoc().add_root(column(table, row(controls1, controls2, controls3),savebutton))

esiid_textbox.on_change('value', lambda attr, old, new: update())
month_slider.on_change('value', lambda attr, old, new:  update())
year_slider.on_change('value', lambda attr, old, new:  update())
tdsp_group.on_change('active', lambda attr, old, new:  update())
to_be_approved.onchange('value', lambda attr, old, new: update())

update()
