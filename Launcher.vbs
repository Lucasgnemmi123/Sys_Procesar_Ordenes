Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener el directorio actual del script
strScriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambiar al directorio del script ANTES de ejecutar Python
objShell.CurrentDirectory = strScriptPath

' Usar Python empaquetado (portable)
pythonExePath = strScriptPath & "\python\python.exe"
pythonwExePath = strScriptPath & "\python\pythonw.exe"

' Verificar que Python empaquetado existe
If Not fso.FileExists(pythonExePath) Then
    MsgBox "Python empaquetado no encontrado en:" & vbCrLf & vbCrLf & _
           pythonExePath & vbCrLf & vbCrLf & _
           "Por favor asegúrate de que la carpeta 'python' esté presente " & _
           "con todos los archivos necesarios.", vbCritical, "Error - Python no encontrado"
    WScript.Quit 1
End If

' Ejecutar el launcher de Python sin ventana (usando pythonw si existe, sino python)
' Usar rutas relativas desde el directorio actual para que los imports funcionen
strPythonCommand = ""
If fso.FileExists(pythonwExePath) Then
    ' Usar pythonw (sin consola) con ruta relativa
    strPythonCommand = "cmd /c cd /d """ & strScriptPath & """ && """ & pythonwExePath & """ launcher.py"
Else
    ' Usar python normal con ruta relativa
    strPythonCommand = "cmd /c cd /d """ & strScriptPath & """ && """ & pythonExePath & """ launcher.py"
End If

On Error Resume Next
objShell.Run strPythonCommand, 0, False
If Err.Number <> 0 Then
    ' Si hay error, mostrar con ventana visible para debug
    Err.Clear
    strPythonCommand = "cmd /c cd /d """ & strScriptPath & """ && """ & pythonExePath & """ launcher.py"
    objShell.Run strPythonCommand, 1, False
    If Err.Number <> 0 Then
        MsgBox "Error al ejecutar el launcher:" & vbCrLf & vbCrLf & _
               Err.Description & vbCrLf & vbCrLf & _
               "Intenta ejecutar:" & vbCrLf & _
               "EXE_Procesar_Ordenes.bat", vbCritical, "Error al Iniciar"
    End If
End If
On Error GoTo 0

Set objShell = Nothing
Set fso = Nothing
