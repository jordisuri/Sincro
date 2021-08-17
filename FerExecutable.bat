rem pyinstaller està en el %PATH%
rem Cal haver generat FSincro.py a partir de FSincro.ui
rem -w fa que no es creï una consola quan s'executi
rem Els dos --add-data copien el text de l'ajuda i la icona a la carpeta de l'executable
rem --noconfirm fa que no es demani una confirmació de sobreescriptura a mig fer,
rem així el pyinstaller només para al final
rem Recordar que l'executable es troba a la carpeta dist

pyinstaller Sincro.py FSincro.py FAjuda.py ModulSincro.py -w --noconfirm --add-data TextAjuda.txt;. --add-data Sincro2.ico;.
