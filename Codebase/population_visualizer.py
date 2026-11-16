import pandas as pd
import matplotlib.pyplot as plt
import os

# Required CSV columns
REQUIRED_COLUMNS = ["City", "Year", "Population"]


# 1. Load and clean population data
def load_data():

    try:
        file_path = "population.csv"

        if not os.path.exists(file_path):
            raise FileNotFoundError("population.csv file not found!")

        df = pd.read_csv(file_path)

        if df.empty:
            print("Error: CSV file is empty!")
            return None

        # Check required columns
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            print("Error: Required CSV columns are missing!")
            return None

        # Clean city names
        df["City"] = df["City"].astype("string").str.strip()

        df = df.dropna(subset=["City"])
        df = df[df["City"] != ""]

        # Convert Year and Population into numeric values
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df["Population"] = pd.to_numeric(
            df["Population"], errors="coerce"
        )

        # Check valid years
        valid_year = (
            df["Year"].notna() &
            (df["Year"] > 0) &
            (df["Year"] % 1 == 0)
        )

        # Check valid population
        valid_population = (
            df["Population"].notna() &
            (df["Population"] > 0) &
            (df["Population"] % 1 == 0)
        )

        # Remove invalid records
        invalid_rows = ~(valid_year & valid_population)

        for index in df.index[invalid_rows]:
            print(f"Invalid record at row {index + 2} rejected.")

        df = df[valid_year & valid_population].copy()

        # Convert values to integers
        df["Year"] = df["Year"].astype(int)
        df["Population"] = df["Population"].astype(int)

        # Remove duplicate records
        before = len(df)

        df = df.drop_duplicates(
            subset=["City", "Year", "Population"]
        )

        removed = before - len(df)

        if removed > 0:
            print(f"{removed} duplicate records removed.")

        if df.empty:
            print("Error: No valid records available!")
            return None

        print("\nPopulation data loaded successfully!")
        print("Valid records:", len(df))

        return df

    except FileNotFoundError as e:
        print("Error:", e)

    except PermissionError:
        print("Error: File permission denied!")

    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty!")

    except pd.errors.ParserError:
        print("Error: CSV file format is incorrect!")

    except Exception as e:
        print("Unexpected error:", e)

    return None


# 2. Calculate population summary
def show_summary(df):

    try:
        latest_year = df["Year"].max()

        latest_data = df[df["Year"] == latest_year]

        total = latest_data["Population"].sum()

        largest = latest_data.loc[
            latest_data["Population"].idxmax()
        ]

        print("\n------ POPULATION SUMMARY ------")

        print("Latest Year:", latest_year)

        print("Total Population:", int(total))

        print(
            "Largest City:",
            largest["City"],
            "(" + str(int(largest["Population"])) + ")"
        )

    except Exception as e:
        print("Error calculating summary:", e)


# 3. Calculate city-wise population growth
def calculate_growth(df):

    growth_list = []

    for city in df["City"].unique():

        city_data = df[
            df["City"] == city
        ].sort_values("Year")

        # Growth requires at least two different years
        if city_data["Year"].nunique() < 2:
            print(f"{city}: Growth not available.")
            continue

        first = city_data.iloc[0]["Population"]
        last = city_data.iloc[-1]["Population"]

        if first <= 0:
            continue

        growth = ((last - first) / first) * 100

        growth_list.append((city, growth))

    return growth_list


# 4. Show growth and fastest-growing city
def show_growth(df):

    growth_list = calculate_growth(df)

    print("\n------ POPULATION GROWTH ------")

    if not growth_list:
        print("Growth not available (only one year of data).")
        return None

    for city, growth in growth_list:
        print(f"{city}: {growth:+.2f}%")

    fastest = max(growth_list, key=lambda x: x[1])

    print(
        "\nFastest-Growing City:",
        fastest[0],
        f"({fastest[1]:+.2f}%)"
    )

    return growth_list


# 5. Generate Bar Chart
def show_bar_chart(growth_list):

    try:
        if not growth_list:
            print("No growth data available for Bar Chart.")
            return

        cities = [item[0] for item in growth_list]
        growth = [item[1] for item in growth_list]

        plt.figure(figsize=(9, 5))

        plt.bar(cities, growth)

        plt.title("Population Growth by City")
        plt.xlabel("City")
        plt.ylabel("Population Growth (%)")

        plt.axhline(y=0, color="black", linewidth=0.8)
        plt.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error generating Bar Chart:", e)


# 6. Generate Line Chart
def show_line_chart(df):

    try:
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

        plt.title("Population Trend Over the Years")
        plt.xlabel("Year")
        plt.ylabel("Population")

        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error generating Line Chart:", e)


# 7. Growth and Charts menu option
def show_charts(df):

    growth_list = show_growth(df)

    show_bar_chart(growth_list)

    show_line_chart(df)


# 8. Main menu
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

            show_charts(df)

        elif choice == "3":

            print("\nThank you for using Population Data Visualizer!")
            break

        else:

            print("Invalid choice! Please enter 1, 2 or 3.")


# 9. Run the program
if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    except Exception as e:
        print("Unexpected runtime error:", e)
