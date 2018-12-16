Sub tickerct()

' I don't care if Brian has 37 pieces of flair (and a great smile)
' I'm only doing the minimum. 
'
' 15 pieces of flair = The Easy + Challenge assignments 


Dim ws As Worksheet

'Challenge assignment
For Each ws In Worksheets
    Dim lastrow As Double
    lastrow = ws.Cells(Rows.Count, "A").End(xlUp).Row
    Dim ticker As String
    Dim summaryrow As Integer
    summaryrow = 2
    Dim tvol As Double
    tvol = 0
    ws.Range("I1").Value = "Ticker"
    ws.Range("J1").Value = "Volume"
    
    'Basic assignment
    For i = 2 To lastrow
        If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then
            ticker = ws.Cells(i, 1).Value
            tvol = tvol + ws.Cells(i, 7).Value
            ws.Range("I" & summaryrow).Value = ticker
            ws.Range("J" & summaryrow).Value = tvol
            summaryrow = summaryrow + 1
            tvol = 0
        Else
            tvol = tvol + ws.Cells(i, 7).Value
        End If
    Next i

Next ws
End Sub

