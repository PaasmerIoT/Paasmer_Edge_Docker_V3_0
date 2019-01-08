void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() 
{
  // put your main code here, to run repeatedly:
  int b,j,i=0;
  String x,c,a,y;
  if (a = Serial.readStringUntil('*'))
  {
    Serial.print(a);
    if (a.substring(0,8) == "Read pin")
    {
      c = a.substring(9,10);
      j = c.toInt();
      b = sensor_read(j);
      Serial.print(b);
      }
    else
    {
      if (a.substring(0,4) == "GPIO")
      {
        if(a.substring(7,9) == "on")
        {
          x = a.substring(5,6);
          j = x.toInt();
          Serial.print(j);
          sensor_write(j,HIGH);
          }
        else if (a.substring(7,10) == "off")
        {
          x = a.substring(5,6);
          j= x.toInt();
          sensor_write(j,LOW);
          }
         }
        }
        delay(2000);
    }
}

int sensor_read(int pin)
{
  int a;
  pinMode(pin,INPUT);
  a = digitalRead(pin);
  return a;
}

void sensor_write(int pin,int state)
{
  pinMode(pin,OUTPUT);
  digitalWrite(pin,state);
}
