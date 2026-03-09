' ========================================
' Sistema de Procesamiento de Pedidos DHL
' Iniciador Silencioso (Sin Consola)
' ========================================

Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")

' Obtener directorio del script
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)

' Archivo principal
MainFile = ScriptDir & "\gui_moderna_v2.py"

' Verificar que existe el archivo principal
If Not FSO.FileExists(MainFile) Then
    MsgBox "No se encontró gui_moderna_v2.py" & vbCrLf & vbCrLf & "Ubicación esperada:" & vbCrLf & MainFile, vbCritical, "Error - Sistema DHL"
    WScript.Quit 1
End If

' Usar Python empaquetado (prioridad 1 - incluye todas las librerías)
PythonCmd = ScriptDir & "\python\python\pythonw.exe"

If Not FSO.FileExists(PythonCmd) Then
    ' Fallback: Python empaquetado con python.exe
    PythonCmd = ScriptDir & "\python\python\python.exe"
End If

If Not FSO.FileExists(PythonCmd) Then
    ' Buscar Python en el sistema (menos probable que funcione)
    PythonCmd = ""
    
    ' Intentar pythonw.exe primero (sin consola)
    On Error Resume Next
    PythonCmd = WshShell.RegRead("HKEY_CURRENT_USER\Software\Python\PythonCore\3.12\InstallPath\")
    If PythonCmd <> "" Then
        PythonCmd = PythonCmd & "pythonw.exe"
        If Not FSO.FileExists(PythonCmd) Then
            PythonCmd = ""
        End If
    End If
    On Error Goto 0

    ' Si no encontró Python 3.12, buscar cualquier versión
    If PythonCmd = "" Then
        On Error Resume Next
        PythonCmd = WshShell.RegRead("HKEY_CURRENT_USER\Software\Python\PythonCore\3.11\InstallPath\")
        If PythonCmd <> "" Then PythonCmd = PythonCmd & "pythonw.exe"
        On Error Goto 0
    End If

    ' Buscar en PATH como último recurso
    If PythonCmd = "" Or Not FSO.FileExists(PythonCmd) Then
        ' Probar pythonw.exe directamente (debe estar en PATH)
        PythonCmd = "pythonw.exe"
    End If
End If

' Ejecutar el sistema
WshShell.CurrentDirectory = ScriptDir
WshShell.Run """" & PythonCmd & """ """ & MainFile & """", 0, False

' 0 = Ocultar ventana
' False = No esperar a que termine

Set WshShell = Nothing
Set FSO = Nothing
