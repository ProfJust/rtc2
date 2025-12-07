ROS2 Jazzy, Gazebo Harmonic

Um den Range Sensor zum TB3 hinzuzufügen

die originalen Files durch diese hier ersetzen 

1.) URDF File    (enthält Joint und Link für den Range Sensor und ein graues Visual Kästchen, dass im RViZ zu sehen ist)

2.) Model.sdf     => Für Gazebo Harmonic nutzt man jetzt eine Kopie des Laserscanners mit anderen Parametern als Range Sensor

3.) Gazebo - ROS2 Bridge: Ergänzen des Topics range in der Liste der Topics im Yaml-File unter Param