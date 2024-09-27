from datetime import datetime
#imported this after as a fallback incase date cannot be pulled from api
import requests
#used so I can utilise the two free APIs in my console

# Main function that includes all logic
def main():
    print("Welcome to your daily horoscope!\n")

    list_star_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                       'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

    while True:
        sign = input(f"Please enter your star sign from {list_star_signs}: ").lower()
        # Allow matching with abbreviation (string slicing)
        for star_sign in list_star_signs:
            # Will match the first three letters provided by user for any sign inputted
            if sign[:3] == star_sign[:3]:
                sign = star_sign
                break

        if sign == 'exit':
            print("See you soon! May the stars be in your favour")
            break

        if sign not in list_star_signs:
            print("Invalid sign. Try again to align the stars.")
            continue

        # To get daily horoscope
        # I found a free horoscope API signed up to subscribe to a free user account
        # used the 'boiler' code they provided on via the api & .get to get info needed
        # access key and url added so info from API can be pulled
        url = 'https://best-daily-astrology-and-horoscope-api.p.rapidapi.com/api/Detailed-Horoscope/'
        querystring = {"zodiacSign": sign}
        headers = {
            "x-rapidapi-key": "a12ccdfd47msh178bdb008ddac14p156831jsn62aac2e2dab7",
            "x-rapidapi-host": "best-daily-astrology-and-horoscope-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            horoscope_info = response.json()
            # Added as a debug check so aware of what to ask to return
            # Tested & removed from live code (kept in code to show how I did de-bug)
            # print("API Response:", horoscope_info)

            # Added as a back-up to ensure API can supply horoscope based current date
            date = datetime.today().strftime('%Y-%m-%d')

            # Checked via the API the parameters I need to .get from
            # Using N/A as a placeholder if api does provide data so console will still run
            your_horoscope = {
                "prediction": horoscope_info.get('prediction', 'N/A'),
                "lucky_number": horoscope_info.get('number', 'N/A'),
                "color": horoscope_info.get('color', 'N/A'),
                "strength": horoscope_info.get('strength', 'N/A'),
                "weakness": horoscope_info.get('weakness', 'N/A'),
            }
        else:
            your_horoscope = {"Error": "Looks like the stars are not aligned - horoscope not available"}
            #Added for de-bugging (this API only provides 18 free uses)
            print(f"Error: Unable to fetch horoscope (Status Code: {response.status_code})")

        if "Error" in your_horoscope:
            print("Error: Looks like the stars are not aligned")
        else:
            # Matching returns in list below with the dictionary linked to the horoscope API
            print(f"\nHoroscope for {sign.capitalize()}:\n")
            print(f"Prediction: {your_horoscope['prediction']}")
            print(f"Lucky Numbers: {your_horoscope['lucky_number']}")
            print(f"Colors: {your_horoscope.get('color', 'No color available')}")
            print(f"Strengths: {your_horoscope['strength']}")
            print(f"Weaknesses: {your_horoscope['weakness']}\n")

            # Save results to a file
            with open('final_results.txt', 'a') as file:
                file.write(f"\nHoroscope for {sign.capitalize()} on {date}:\n")
                file.write(f"Prediction: {your_horoscope['prediction']}\n")
                file.write(f"Lucky Numbers: {your_horoscope['lucky_number']}\n")
                file.write(f"Colors: {your_horoscope.get('color', 'No color available')}\n")
                file.write(f"Strengths: {your_horoscope['strength']}\n")
                file.write(f"Weaknesses: {your_horoscope['weakness']}\n")
                file.write('\n' + '-' * 40 + '\n')

            # Added 2nd API to get image based on the color returned for horoscope API
            # Creative :)
            # This API free all the time 'easier' to add to code
            color = your_horoscope.get('color', None)
            if color:
                access_key = 'P57Yugo7lJuXZe5DOmsO10Q2g7NltdRR2NdLB_u9iQc'
                url = f'https://api.unsplash.com/photos/random?query={color}&client_id={access_key}'

                response = requests.get(url)
                if response.status_code == 200:
                    image_data = response.json()
                    if 'urls' in image_data:
                        #This means the images provided will be high-quality smaller sized image
                        mood_image_url = image_data['urls']['regular']
                        print(f"\nYour mood color is ({your_horoscope['color']}) - here's an image based on your mood: {mood_image_url}")
                        print("To view, open the link in a browser.")

                        # Writing image URL to the file
                        with open('final_results.txt', 'a') as file:
                            file.write(f"\nYour mood color is ({your_horoscope['color']}) - here's an image based on your mood: {mood_image_url}")
                            file.write('\n' + '-' * 40 + '\n')
                    else:
                        print("Error: Image URL not available")
                else:
                    print("Error: Looks like the stars are not aligned")
            # Added last else in case there is no color match from prior horoscope API
            else:
                print("No color available for this sign, so no image can be retrieved.")

        # Added option to continue in the while loop or exit
        cont = input("\nHow about checking out another star sign? (yes/no): ").lower()
        if cont != 'yes':
            print("See you later! May the stars be in your favour.")
            break

if __name__ == "__main__":
    main()

