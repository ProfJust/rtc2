
echo "$TURTLEBOT3_MODEL"

if [ "$TURTLEBOT3_MODEL" = "burger" ]; then
  echo "Das Modell ist burger."
else
  echo "Burger wird eingestellt"  
  echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
  source ~/.bashrc
fi

# Wenn ein Shell-Skript beendet wird, gehen Variablen verloren, 
# die darin neu gesetzt wurden (außer sie werden vor dem Skriptstart exportiert
# oder persistent in .bashrc eingetragen).
