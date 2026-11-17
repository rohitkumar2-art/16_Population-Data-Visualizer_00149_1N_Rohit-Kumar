import pandas as pd
import matplotlib.pyplot as plt
import os


# CSV file location
FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "population.csv"
)


# 1. Load and clean population data
def load_data():

    try:
        df = pd.read_csv(FILE_PATH)

        # Check empty CSV
        if df.empty:
            print("Error: CSV file is empty!")
            return None

        # Check required columns
        required = ["City", "Year", "Population"]

        if not all(col in df.columns for col in required):
            print("Error: CSV columns are incorrect!")
            return None

        valid_records = []

        # Validate each row
        for row_number, (_, row) in enumerate(
            df.iterrows(), start=1
        ):

            city = row["City"]
            year = row["Year"]
            population = row["Population"]

            # Check city name
            if pd.isna(city) or str(city).strip() == "":
                print(f"Row {row_number} skipped: City name missing.")
                continue

            city = str(city).strip()

            # Validate year
            try:
                year = float(year)

                if pd.isna(year) or year <= 0 or not year.is_integer():
                    print(
                        f"Row {row_number} skipped: "
                        f"Year must be a positive integer."
                    )
                    continue

            except (ValueError, TypeError):
                print(
                    f"Row {row_number} skipped: invalid Year '{row['Year']}'."
                )
                continue

            # Validate population
            try:
                population = float(population)

                if pd.isna(population):
                    print(
                        f"Row {row_number} skipped: "
                        f"invalid Population '{row['Population']}'."
                    )
                    continue

                if population <= 0:
                    print(
                        f"Row {row_number} skipped: "
                        f"Population must be positive."
                    )
                    continue

            except (ValueError, TypeError):
                print(
                    f"Row {row_number} skipped: "
                    f"invalid Population '{row['Population']}'."
                )
                continue

            # Store valid records
            valid_records.append({
                "City": city,
                "Year": int(year),
                "Population": population
            })

        # Create cleaned DataFrame
        clean_df = pd.DataFrame(
            valid_records,
            columns=required
        )

        # Remove duplicate records
        clean_df = clean_df.drop_duplicates(
            subset=["City", "Year", "Population"]
        )

        print("\nPopulation data loaded successfully!")
        print("Valid records:", len(clean_df))

        if clean_df.empty:
            print("No valid population records found!")
            return None

        return clean_df

    except FileNotFoundError:
        print("Error: population.csv file not found!")
        return None

    except PermissionError:
        print("Error: Permission denied while reading CSV file!")
        return None

    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty!")
        return None

    except pd.errors.ParserError:
        print("Error: CSV file format is incorrect!")
        return None

    except Exception as e:
        print("Unexpected error:", e)
        return None


# 2. Calculate city-wise population growth
def calculate_growth(df):

    growth_list = []

    for city in df["City"].unique():

        city_data = df[
            df["City"] == city
        ].sort_values("Year")

        # Growth requires at least two different years
        if city_data["Year"].nunique() < 2:
            continue

        first = city_data.iloc[0]["Population"]
        last = city_data.iloc[-1]["Population"]

        if first <= 0:
            continue

        growth = ((last - first) / first) * 100

        growth_list.append((city, growth))

    return growth_list


# 3. Calculate and display population summary
def show_summary(df):

    try:
        latest_year = df["Year"].max()

        latest_data = df[
            df["Year"] == latest_year
        ]

        total = latest_data["Population"].sum()

        largest = latest_data.loc[
            latest_data["Population"].idxmax()
        ]

        print("\n------ POPULATION SUMMARY ------")

        print("Latest Year:", int(latest_year))

        print("Total Population:", int(total))

        print(
            "Largest City:",
            largest["City"],
            "(" + str(int(largest["Population"])) + ")"
        )

        # Find fastest-growing city
        growth_list = calculate_growth(df)

        if growth_list:

            fastest = max(
                growth_list,
                key=lambda x: x[1]
            )

            print(
                "Fastest growing:",
                fastest[0],
                f"({fastest[1]:+.2f}%)"
            )

        else:
            print(
                "Growth: not available "
                "(only one year of data)"
            )

    except Exception as e:
        print("Error calculating summary:", e)


# 4. Show city-wise growth and charts
def show_growth_and_charts(df):

    try:
        growth_list = calculate_growth(df)

        print("\n------ POPULATION GROWTH ------")

        if growth_list:

            for city, growth in growth_list:
                print(f"{city}: {growth:+.2f}%")

            fastest = max(
                growth_list,
                key=lambda x: x[1]
            )

            print(
                "\nFastest-Growing City:",
                fastest[0],
                f"({fastest[1]:+.2f}%)"
            )

            # Bar Chart: Population Growth by City
            cities = [
                item[0] for item in growth_list
            ]

            growth_values = [
                item[1] for item in growth_list
            ]

            plt.figure(figsize=(9, 5))

            plt.bar(cities, growth_values)

            plt.title("Population Growth by City")
            plt.xlabel("City")
            plt.ylabel("Growth Percentage (%)")

            plt.grid(axis="y")
            plt.tight_layout()
            plt.show()

        else:
            print(
                "Growth not available "
                "(only one year of data)."
            )

        # Line Chart: Population Trend
        plt.figure(figsize=(9, 5))

        for city in df["City"].unique():

            city_data = df[
                df["City"] == city
            ].sort_values("Year")

            plt.plot(
                city_data["Year"],
                city_data["Population"],
                marker="o",
                label=city
            )

        plt.title("Population Trend")
        plt.xlabel("Year")
        plt.ylabel("Population")

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error displaying charts:", e)


# 5. Main menu
def main():

    df = load_data()

    if df is None:
        return

    while True:

        print("\n================================")
        print("    POPULATION DATA VISUALIZER")
        print("================================")

        print("1. Population Summary")
        print("2. Growth and Charts")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":

            show_summary(df)

        elif choice == "2":

            show_growth_and_charts(df)

        elif choice == "3":

            print("Thank you! Program closed.")
            break

        else:

            print("Invalid choice! Please enter 1, 2 or 3.")


# Run the program
if __name__ == "__main__":
    main()

