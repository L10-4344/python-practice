print("Wut Doo Ah Wehr™ - clothing suggestions for the day's weather")
print("")
while True:
    try:
        temperature = int(input("What's the temperature in °C? "))

        if abs(temperature) > 100000:
            print("")
            print("Mate, if the temperature is above 100,000°C or below -100,000°C, clothing is no longer the primary concern.")

        break
    except ValueError:
        print("")
        print("Please enter integers only.")

if temperature >= -100000 and temperature <= -273:
  print("At these temperatures, the sun would freeze.")
  print("...")
  print("Well, not really. The only way the sun could ever freeze is if it loses all it's energy. But that's not as fun to say.")
  print("...")
  print("Yes, I realise I just said it.")

elif -272 <= temperature <= -100:
  print("At this temperature, your skin will freeze in mere seconds and breathing will send you into cardiac arrest immediately. And once you die (which will happen in a couple seconds), your blood will freeze.")

elif -99 <= temperature <= -23:
    print("It's not the ice age, bro.")

elif -22 <= temperature <= -16:
    print("Are you in Antarctica?")

elif -15 <= temperature <= -10:
    print("Rug up properly. It's absolutely freezing.")

elif -9 <= temperature <= -1:
    print("Wear a heavy coat, gloves and a beanie.")

elif 0 <= temperature < 5:
    print("")
    print("Wear a warm coat, long pants and maybe a beanie.")

elif 5 <= temperature <= 14:
    print("")
    print("Wear a hoodie, it's chilly.")

elif 15 <= temperature < 25:
    print("")
    print("Wear a T-shirt and trousers.")

elif 25 <= temperature < 35:
    print("")
    print("Wear a T-shirt and shorts.")

elif 35 <= temperature <= 50:
    print("")
    print("T-shirt, shorts, hat and sunscreen, it's pretty hot.")
    print("Don't forget to drink lots of water!")

elif 50 < temperature < 60:
    print("")
    print("Damn, that's pretty bloody hot.")

elif 60 <= temperature < 80:
    print("")
    print("Mate, stay inside")

elif 80 <= temperature < 100:
    print("")
    print("You might want to check whether you're on Venus or not...")

elif 100 <= temperature <= 100000:
    print("")
    print("The laws of nature have officially stopped cooperating. Rest in peace, mate.")

print("")
print("Thank you for using Wut Doo Ah Wehr™!")