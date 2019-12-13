const int Wpin = 34;
const int BLpin = 35;
const int TRpin = 25;
const int BRpin = 26 ;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read analog inputs
  float Wval = analogRead(Wpin);
  float TRval = analogRead(TRpin);
  float BLval = analogRead(BLpin);
  float BRval = analogRead(BRpin);

  // Convert analog reading (goes from 0 - 4096) to voltage (0 - 3.3V):
  float Wvoltage = Wval * (3.3 / 4095.0);
  float TRvoltage = TRval * (3.3 / 4095.0);
  float BLvoltage = BLval * (3.3 / 4095.0);
  float BRvoltage = BRval * (3.3 / 4095.0);

  // Print voltages to serial
  Serial.print(Wvoltage);
  Serial.print("--");
  Serial.print(TRvoltage);
  Serial.print("--");
  Serial.print(BLvoltage);
  Serial.print("--");
  Serial.println(BRvoltage);
}
