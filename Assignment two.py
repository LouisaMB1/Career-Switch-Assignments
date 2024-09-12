from datetime import datetime
import requests

# Main function that includes all logic
def main():
    print("Welcome to your daily horoscope!\n")

    list_star_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                       'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

    while True:
        sign = input(f"Please enter your star sign from {list_star_signs}: ").lower()

        if sign == 'exit':
            print("See you soon! May the stars be in your favour")
            break

        if sign not in list_star_signs:
            print("Invalid sign. Try again to align the stars.")
            continue

        # Get daily horoscope
        url = 'https://best-daily-astrology-and-horoscope-api.p.rapidapi.com/api/Detailed-Horoscope/'
        querystring = {"zodiacSign": sign}
        headers = {
            "x-rapidapi-key": "a12ccdfd47msh178bdb008ddac14p156831jsn62aac2e2dab7",
            "x-rapidapi-host": "best-daily-astrology-and-horoscope-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            horoscope_info = response.json()
            print("API Response:", horoscope_info)  # Added as a debug check so aware of what to ask to return

            date = datetime.today().strftime('%Y-%m-%d')

            your_horoscope = {
                "prediction": horoscope_info.get('prediction', 'N/A'),
                "lucky_number": horoscope_info.get('number', 'N/A'),
                "color": horoscope_info.get('color', 'N/A'),
                "strength": horoscope_info.get('strength', 'N/A'),
                "weakness": horoscope_info.get('weakness', 'N/A'),
            }
        else:
            your_horoscope = {"Error": "Looks like the stars are not aligned - horoscope not available"}
            print(f"Error: Unable to fetch horoscope (Status Code: {response.status_code})")

        if "Error" in your_horoscope:
            print("Error: Looks like the stars are not aligned")
        else:
            print(f"\nHoroscope for {sign.capitalize()}:\n")
            print(f"Prediction: {your_horoscope['prediction']}")
            print(f"Lucky Numbers: {your_horoscope['lucky_number']}")
            print(f"Colors: {your_horoscope.get('color', 'No color available')}")
            print(f"Strengths: {your_horoscope['strength']}")
            print(f"Weaknesses: {your_horoscope['weakness']}\n")

            # Get image based on the color returned
            color = your_horoscope.get('color', None)
            if color:
                access_key = 'P57Yugo7lJuXZe5DOmsO10Q2g7NltdRR2NdLB_u9iQc'
                url = f'https://api.unsplash.com/photos/random?query={color}&client_id={access_key}'

                response = requests.get(url)
                if response.status_code == 200:
                    image_data = response.json()
                    if 'urls' in image_data:
                        mood_image_url = image_data['urls']['regular']
                        print(f"\nYour mood color is ({your_horoscope['color']}) - here's an image based on your mood: {mood_image_url}")
                        print("To view, open the link in a browser.")
                    else:
                        print("Error: Image URL not available")
                else:
                    print("Error: Looks like the stars are not aligned")
            else:
                print("No color available for this sign, so no image can be retrieved.")

        # Option to continue in the while loop or exit
        cont = input("\nHow about checking out another star sign? (yes/no): ").lower()
        if cont != 'yes':
            print("See you later! May the stars be in your favour.")
            break

if __name__ == "__main__":
    main()

