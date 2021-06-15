############################################
# ASSOCIATION RULE LEARNING (BİRLİKTELİK KURALI ÖĞRENİMİ)
############################################
# Amacımız online retail II veri setine birliktelik analizi uygularak kullanıcılara ürün satın alma sürecinde ürün önermek.

# Değişkenler
# InvoiceNo: Fatura Numarası , Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.
# StockCode: Ürün kodu, Her bir ürün için eşsiz numara.
# Description: Ürün İsmi
# Quantity: Ürün Adedi, Faturlardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura Tarihi
# UnitPrice: Fatura fiyatı(sterlin)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi


import pandas as pd
pd.set_option('display.max_columns', None) # bütün sütunları göster
#pd.set_option('display.max_rows', None)   # bütün satırları göster
pd.set_option('display.width', 500)        # yan yana 500 tane göster
pd.set_option('display.expand_frame_repr', False)  # çıktının tek bir satırda olmasını sağlar.
from mlxtend.frequent_patterns import apriori, association_rules

df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = df_.copy()
df.head()

######################################################
# GÖREV 1:
######################################################
# Veri Ön İŞleme İşlemlerini Gerçekleştirme

###########################
# Veri öN iŞLEME
###########################
from helpers.helpers import check_df, retail_data_prep
check_df(df)

###########################
# Veri Ön İşleme Sonrası
###########################
df = retail_data_prep(df)   # veriyi temizler.
check_df(df)

######################################################
# GÖREV 2:
######################################################
# Germany müşterileri üzerinden birliktelik kuralları üretme.

df_grmny = df[df['Country'] == "Germany"]
check_df(df_grmny)   # indirgediğimiz veri setinin yapısal bilgileri

# Faturalara sepet muamelesi yapılacak ve 1 sepette bu ürünlerden varsa 1 yoksa 0 yazılacak.

# 1. YOL
def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.pivot_table(values='Quantity', index="Invoice", columns="StockCode", aggfunc="sum").fillna(0).applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.pivot_table(values='Quantity', index="Invoice", columns="Description", aggfunc="sum").fillna(0).applymap(lambda x: 1 if x > 0 else 0)

# Bu matrix'ler seyrek matrix'ler olarak geçer. Bazı problemlerin temelini oluşturur.
# Buradaki her bir invoice bir fatura bu faturalarda bu ürün var mı yok mu diyerek binary encoding ettik.
grmnyi_inv_pro_df = create_invoice_product_df(df_grmny, id=True)
grmnyi_inv_pro_df.head()

# 2. YOL
def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

grmny_inv_pro_df = create_invoice_product_df(df_grmny, id=True)
grmny_inv_pro_df.head()

# Denemelik
df1 = df[df["Invoice"] == 536983]
df1

df1.groupby(['Invoice', 'Description']).agg({"Quantity": "count"}).unstack()

df[(df["StockCode"] == 22331) & (df["Invoice"] == 536983)]

###########################
# Birliktelik Kuralının Çıkarılması
###########################

# Tüm olası ürün birlikteliklerinin olasılıkları için apriori fonksiyonu:
grmny_frequent_itemsets = apriori(grmny_inv_pro_df, min_support=0.01, use_colnames=True)

# Bunlar ürünlerin tek başlarına gözükme olasılıklarıdır.
grmny_frequent_itemsets.sort_values("support", ascending=False)   # Support değerine göre azalan bir şekilde sıralama işlemi.

# Yukarda apriori ile sadece support'ları hesapladık.
# association_rules ile diğer bütün metrikleri hesaplama işlemi:
grmny_rules = association_rules(grmny_frequent_itemsets, metric="support", min_threshold=0.01)
grmny_rules.sort_values("support", ascending=False).head()  # 2 ürünün birlikte gözükme olasılığına göre veri setinin sıralanması.

# * antecedents: önceki ürün
# * consequents: sonraki ürün
# * antecedent_support: önceki ürünün tek başına olasılığı
# * consequent_support: sonraki ürünün tek başına olasılığı
# * support: 2 ürünün birlikte olasılığı
# * confidence: birisi alındığında diğerinin alınma olasılığı
# * leverage: kaldıraç etkisi, pratikte lift kullanılır çünkü leverage support'u yüksek olan değerlere öncelik verme eğilimi vardır.
# * lift ise daha az sıklıklara rağmen gizlenmiş ilişkileri bulabilmektedir.


######################################################
# GÖREV 3:
######################################################
# ID'leri verilen ürünlerin isimleri neledir?
# Kullanıcı 1 ürün id'si: 21987
# Kullanıcı 2 ürün id'si: 23235
# Kullanıcı 3 ürün id'si: 22747

df_grmny[df_grmny["StockCode"] ==  21987][["Description"]].values[0].tolist()  # Bu şekilde de gelir bu aşağıda fonksiyonlaştırıldı.

# hangi id hangi ürüne ait fonksiyonu
def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(df_grmny, 21987)

check_id(df_grmny, 23235)

check_id(df_grmny, 22747)

######################################################
# GÖREV 4:
######################################################
# Sepetteki kullanıcılar için ürün önerisi yapınız.

# Örnek olarak böyle bir kullanıcı geldi ve bu kullanıcı login oldu bir ürüne bakıyor ve sepetine ekledi dedik.

product_id = 23235
check_id(df, product_id)  # ilk baştaki dataframe

sorted_rules = grmny_rules.sort_values("lift", ascending=False)   # Kolaylık olsun diye ürünleri lift'e göre sıraladık.
sorted_rules.shape
sorted_rules.head()

# rec_count: gözlem birimi sayısı
def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id and list(sorted_rules.iloc[i]["consequents"])[0] not in recommendation_list:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]

a = arl_recommender(grmny_rules, 23235, 2)   # Tekrar edenleri içine katılmadı fonksiyon içerisinde elendi.
a

b = arl_recommender(grmny_rules, 21987, 4)
b

c = arl_recommender(grmny_rules, 22747, 3)
c

check_id(df, a[1])
######################################################
# GÖREV 5:
######################################################
# Önerilen ürünlerin isimleri nelerdir?

list = [a, b, c]
for i, x in enumerate(list):
    print(F" {x[1]} ".center(50, "*"))
    xx = df_grmny[df_grmny["StockCode"] == x[1]][["Description"]].values[0]
    print(xx)
