# 🚀 Iniciar el Sistema

## Forma Recomendada

Haz **doble clic** en el acceso directo:

```
📁 Sistema Procesar Pedidos.lnk
```

Este acceso directo:
- ✅ Tiene el ícono del sistema
- ✅ Inicia el sistema sin mostrar consola
- ✅ Usa rutas relativas (funciona en cualquier máquina)
- ✅ Está versionado en Git

## ¿Cómo usarlo?

1. **Desde aquí**: Doble clic directo en el acceso directo
2. **Copiar al escritorio**: Arrastra el acceso directo a tu escritorio
3. **Anclar a barra de tareas**: Clic derecho → Anclar a la barra de tareas

## Otras formas de iniciar

### Desde terminal (con consola visible)
```bash
python gui_moderna_v2.py
```

### Desde PowerShell (sin consola)
```powershell
pythonw gui_moderna_v2.py
```

## Notas Técnicas

- El acceso directo ejecuta `Iniciar_Sistema.vbs`
- El VBS ejecuta `gui_moderna_v2.py` con pythonw (sin consola)
- El ícono viene de `launcher_icon.ico`
- Todo usa rutas relativas para portabilidad

## Si el acceso directo no funciona

Ejecuta este script para recrearlo:
```powershell
.\Crear_Acceso_Directo.ps1
```

---

**Sistema de Procesamiento de Pedidos v3.0**  
Created by Lucas Gnemmi
