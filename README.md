# ASSOCIATION_RULE_LEARNING
* Bir veri öğesinin başka bir veri öğesine bağımlılığını kontrol eden ve daha kararlı olabilmesini sağlayan kural tabanlı bir makine öğrenmesi tekniğidir. 
* Ayrıca geçmiş verilerin analizini sağlayarak keşfettiği ilişkiler ile geleceğe yönelik çalışmaların yapılmasını destekler. 

     ![image](https://user-images.githubusercontent.com/73841520/122132425-7bcb8c00-ce43-11eb-88cb-1e3bf4f5384c.png)
     
* Örneğin, bir müşteri ekmek satın alırsa, büyük bir olasılıkla süt, tereyağı veya yumurta alabilir. 
* Bu sebeple bu ürünler aynı rafta ya da çoğunlukla yakınlarda tutulur. Bu durum Birliktelik Kuralı ile gösterilir ve ürün önerileri yapılmasını sağlar.

# APRİORİ ALGORİTMASI 
* Apriori algoritması, Agrawal ve Srikant tarafından 1994 yılında ortaya çıkmıştır.
* Bu algoritmanın ismi, bilgileri bir önceki adımdan aldığından «prior» anlamında Apriori’dir.
* Öğe kümesi(itemset): Bir veya daha çok öğeden oluşan küme
* K-öğe kümesi(k-itemset): k öğeden oluşan küme(Ekmek, Süt, Tereyağı)
* Apriori algoritmasına göre temel yaklaşım, eğer k-öğe kümesi minimum destek değerini sağlıyorsa, bu kümenin alt kümeleri de minimum destek kriterini sağlar.

     ![image](https://user-images.githubusercontent.com/73841520/122132604-cc42e980-ce43-11eb-8aa2-761bfbe2a39c.png)

* Birliktelik kuralının ilk aşamasında yaklaşımları gerçekleştirmek için en çok Apriori Algoritması tercih edilir.
* Sepet analiz yöntemidir.
* En çok birlikte alınan ürünleri görmemizi ve buna göre hareket etmemizi sağlar. 

# İŞ PROBLEMİ
* Sepet aşamasındaki kullanıcılara ürün önerisinde bulunmak.

# VERİ SETİ HİKAYESİ
* Online Retail II isimli veri seti İngiltere merkezli online bir satış mağzasının 01/12/2009-09/12/2011 tarihleri arasındaki satışları içeriyor.
* Bu şirketin ürün kataloğundaki hediyelik eşyalar yer alıyor.
* Promosyon ürünleri olarak da düşünülebilir.
* Çoğu müşterisinin toptancı olduğu bilgisi de mevcut

