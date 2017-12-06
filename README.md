# Rattler

## Modeling
- Jedes Model ist eine Klasse, das von `django.db.models.Model` erbt
- Jedes Attribut eines Models ist gleichzeitig ein Feld in der Datenbank

### Models hinzufügen
- Neue Models werden in der `models.py` der jeweiligen App erstellt
- Damit das migirerne funktioniert, muss die App in die Konfiguration `INSTALLED_APPS` hinzugefügt werden

Bsp.: 
In der App user soll ein User Model erstellt werden. Hierfür wird 

apps/user/models.py
```python
from django.db import models

class User(models.Model):
```

Attribute müssen als Django Models Field (`django.db.models.Field`) eingetragen werden.

Bsp.:
Das User Model soll ein Feld Name haben.
```python
class User(models.Model):
    name = models.CharField()
```

### Feld Klassen
#### Default Options
- null: Erlauben von Null Werten (default=false)
- blank: Erlauben von "leeren" Werten oder auch "not-required" (default=false)
- choices: Ein eine Liste von Zweiertupeln, die Gültige Werte enthalten
- default: Default Wert
- primary_key: Als Schlüssel Attribut kenzeichnen
- unique: Als Einzigartig kennzeichnen

#### AutoField, BigAutoField
Ein Integer Feld, der Automatisch hochgezählt wird.
#### BigIntegerField
Ein Integer Feld
#### BooleanField,  NullBooleanField
Ein "True" oder "False" Feld.
Das NullBooleanField erlaubt auch `null` als Wert.
#### CharField
Ein Text Feld.
Options:
 - max_length: Für die länge des Feldes - Required
#### DateField, DateTimeField
Ein Datumsfeld bzw. ein Feld mit Datum und Zeit.
Options:
 - auto_now: Automatisch auf "Jetzt" setzten, bei jedem Speichern des Objektes
 - auto_now_add: Setzt den Wert auf "Jetzt" beim ersten Speichern
#### DecimalField
Ein Feld für fixe Zahlen mit Nachkommer.
Options:
 - max_digits: Anzahl an Vorkommer und Nachkommer Zahlen
 - decimal_places: Anzahl der Nachkommer stellen
#### DurationField
Feld für "Zeitdeltas"
#### EmailField
Wie `CharField`, jedoch mit EMail Validation.
#### FloatField, IntegerField
Feld für Nummern
#### ForeignKey, ManyToManyField
Fremdschlüssel
Bsp.: `foregin = models.ForeignKey(ForeginModel)`
Options:

#### Weitere Felder:
[https://docs.djangoproject.com/en/2.0/ref/models/fields/#field-types](Django Field Types)

### Fremdschlüssel
Fremdschlüssel werden mit dem 
 manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
