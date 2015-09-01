
TODO
====

* Code gen option for python 2 & 3

* Excel Gen has error
      File "D:\py_proj_2015\XYmath\xymath\gui\page_codegen.py", line 162, in GenCode_Button_Click
        did_good = xymath.source_excel.make_fit_excel(obj)
      File "d:\py_proj_2015\xymath\xymath\source_excel.py", line 65, in make_fit_excel
        yLabel=eqnObj.ds.get_y_desc(), xLabel=eqnObj.ds.get_x_desc())
      File "d:\py_proj_2015\xymath\xymath\xlChart.py", line 669, in makeChart
        cRange.Value = rs
      File "C:\Anaconda\lib\site-packages\win32com\client\dynamic.py", line 560, in __setattr__
        self._oleobj_.Invoke(entry.dispid, 0, invoke_type, 0, value)
    com_error: (-2147352567, 'Exception occurred.', (0, None, None, None, 0, -2146827284), None)

* Exit message is confusing (Exit vs Saved???)