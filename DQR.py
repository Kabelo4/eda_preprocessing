
import pandas as pd
import numpy as np

class DataQualityReport:
    def __init__(self, df, continuous, categorical):
        self.conti = df[continuous]
        self.categ = df[categorical]

    # def continuous(self):
    #     report = self.conti.describe().T
    #     report['Card.'] = self.conti.nunique().values
    #     report['Miss%'] = 100 * (self.conti.isnull().sum() / len(self.conti))
    #     column_order = ['count', 'Miss%', 'Card.', 'min', '25%', 'mean', '50%', '75%', 'max', 'std']
    #     report = np.round(report[column_order], 3)
    #     report = report.reset_index()
    #     report = report.rename(columns={report.columns[0]: 'Feature', '50%': 'Median'})
    #     report.columns = [col.capitalize() for col in report.columns]
    #     return report


    def continuous(self):
        # Initialize the report DataFrame
        report = pd.DataFrame()

        # Compute the count of non-null values
        report['Count'] = self.conti.notnull().sum()

        # Compute the cardinality (number of unique values)
        report['Card.'] = self.conti.nunique()

        # Compute the percentage of missing values
        report['Miss%'] = 100 * (self.conti.isnull().sum() / len(self.conti))

        # Compute descriptive statistics
        report['Min'] = self.conti.min()
        report['25%'] = self.conti.quantile(0.25)
        report['Mean'] = self.conti.mean()
        report['50%'] = self.conti.median()
        report['75%'] = self.conti.quantile(0.75)
        report['Max'] = self.conti.max()
        report['Std'] = self.conti.std()

        # Round the results
        report = np.round(report, 3)

        # Reset index to make 'Feature' column
        report = report.reset_index()
        report = report.rename(columns={report.columns[0]: 'Feature'})

        # Capitalize column names
        report.columns = [col.capitalize() for col in report.columns]

        return report
    
    def categorical(self):
        report_data = []

        total_rows = len(self.categ)

        for var in self.categ.columns:
            value_counts = self.categ[var].value_counts()
            mode, freq = value_counts.index[0], value_counts.iloc[0]
            mode_percent = (freq / total_rows) * 100

            mode_2, freq_2 = value_counts.index[1] if len(value_counts) > 1 else None, \
                                  value_counts.iloc[1] if len(value_counts) > 1 else None
            mode_percent_2 = (freq_2 / total_rows) * 100 if mode_2 is not None else None

            report_data.append({
                'Feature': var,
                'Count': total_rows,
                'Miss%': 100 * self.categ[var].isnull().mean(),
                'Card.': self.categ[var].nunique(),
                'Mode': mode,
                'Mode_Freq': freq,
                'Mode%': mode_percent,
                '2nd_Mode': mode_2,
                '2nd_Mode_Freq': freq_2,
                '2nd_Mode%': mode_percent_2,
            })

        report = pd.DataFrame(report_data).round({'Miss%': 3, 'Mode%': 3, '2nd_Mode%': 3})
        return report
