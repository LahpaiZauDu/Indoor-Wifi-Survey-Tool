import pandas as pd

df = pd.read_csv('Data/simple.csv')
channel_values = ['1', '11', '36']
df_sv = df[df.CHANNEL.isin(channel_values)]
five_column = df_sv[['SSID', 'BSSID', 'CHANNEL',
                     'RSSI', 'Xcoordinate', 'Ycoordinate']]

df = five_column
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.to_csv('Data/channel1_11_36.csv', index=False)
