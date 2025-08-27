import numpy as np
import pandas as pd

# Function to clean the data
def clean_data(df: pd.DataFrame)->pd.DataFrame:
    """
    Function to clean the raw data

    """
    # convert the values to crores scale
        
    def convert_to_crores(ser):
            return(
                    ser
                    .str.split(" ",expand = True)
                    .set_axis(["amount","unit"],axis=1)
                    .assign(
                        amount = lambda df:(
                            np.where(
                                df.unit.eq("Lac"),
                                df.amount.astype(float).mul(0.01),
                                df.amount.astype(float)
                            )
                        )
                    )
                    .amount
            )
        
    # all the units converted to sqft

    conversion_factors = {
            "sqft": 1,
            "sqyrd": 9,
            "sqm": 10.7639,
            "marla": 272.25,
            "kanal": 5445,
            "ground": 2400,
            "biswa2": 1350,
            "aankadam": 75,
            "acre": 43560,
            "hectare": 107639,
            "cent": 435.6,
            "bigha": 27225
        }
    
    def remove_area_units_and_standardize(ser):
            return(
                ser
                .str.replace(",","")
                .str.split(" ",expand = True)
                .set_axis(["value","unit"],axis=1)
                .assign(
                    value = lambda df:(
                        pd.to_numeric(df.value)*df.unit.map(conversion_factors)
                    )
                )
                .value
            )
    
    # return the cleaned dataframe

    return (
            df
            .assign(**{
                col: df[col].str.strip()
                for col in df.select_dtypes(include = "O").columns
            })
            .rename(columns = lambda col: col.lower().replace(" ","_").split("_(")[0].split("(")[0])
            .query('amount != "Call for Price"')
            .assign(
                bathroom = lambda df: pd.to_numeric(df.bathroom.str.replace("> ","")),
                balcony = lambda df: pd.to_numeric(df.balcony.str.replace("> ","")),
                amount = lambda df: df.amount.pipe(convert_to_crores),
                carpet_area = lambda df: df.carpet_area.pipe(remove_area_units_and_standardize),
                super_area = lambda df: df.super_area.pipe(remove_area_units_and_standardize),
                floor = lambda df: df.floor.str.replace("200 out of 200","2 out of 2"),
                car_parking = lambda df: df.car_parking.str.replace(",",""),
                num_bhk = lambda df: (
                    pd.to_numeric(
                        np.where(
                            df.title.str.contains("BHK"),
                            df.title.str.split("BHK").str[0].str.replace(">","").str.strip(),
                            np.nan
                    )
                  )
                ),
               floor_num = lambda df: pd.to_numeric(
                    np.where(
                        df.floor.str.contains("out of", na=False),
                        df.floor.str.split("out of").str[0]
                            .str.replace("Ground","0")
                            .str.replace("Lower Basement","0")
                            .str.replace("Upper Basement","0"),
                        np.nan
                    ), errors="coerce"
                ),
               num_floors = lambda df: pd.to_numeric(
                    np.where(
                        df.floor.str.contains("out of", na=False),
                        df.floor.str.split("out of").str[1],
                        np.nan
                    ), errors="coerce"
                ),
               overlooking_garden = lambda df: (
                   np.where(
                       df.overlooking.isnull(),
                       np.nan,
                       np.where(df.overlooking.str.contains("Garden"),1,0)
                   )
               ),
               overlooking_pool = lambda df: (
                   np.where(
                       df.overlooking.isnull(),
                       np.nan,
                       np.where(df.overlooking.str.contains("Pool"),1,0)
                   )
               ),
               overlooking_mainroad = lambda df: (
                   np.where(
                       df.overlooking.isnull(),
                       np.nan,
                       np.where(df.overlooking.str.contains("Main Road"),1,0)
                   )
               ),
               parking_spots = lambda df: (
                   pd.to_numeric(
                       df.car_parking
                       .str.extract(r"(\d+)")[0],
                       errors = 'coerce'
                   )
               ),
               parking_cover = lambda df: (
                       np.where(
                           df.car_parking.isnull(),
                           np.nan,
                           df.car_parking
                           .str.split(" ")
                           .str[1]
                       )
               )
            )
            .assign(
                balcony = lambda df:(
                    np.where(df.floor_num == 0,0,df.balcony)
                )
            )
            .loc[lambda df: (df.carpet_area.between(90,10000)) | (df.super_area.between(100,10000))]
            .loc[lambda df: (df.price.between(200,10000))]
            .loc[lambda df: df.amount.between(0.1,100)]
            .loc[lambda df:
                (
                    df.num_bhk.isnull()
                    | (df.bathroom.isnull() | df.bathroom.lt(df.num_bhk + 2))
                    & (df.balcony.isnull() | df.balcony.lt(df.num_bhk + 2))
                )
            ]
            .loc[lambda df: df.num_floors.ge(df.floor_num)]
            .drop(columns = ["title","floor","overlooking","car_parking","price","index","description","status","society","dimensions","plot_area"])
            .drop_duplicates()
            .dropna(subset = ["transaction","num_bhk","bathroom"])
        )