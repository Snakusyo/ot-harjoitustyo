import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
    
    def test_rahamaara_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_myydyt_lounaat_alussa(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisosto_edullinen_vaihtoraha_toimii(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)

    def test_kateisosto_edullinen_kasvattaa_kassan_arvoja(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateisosto_maukkaat_vaihtoraha_toimii(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)

    def test_kateisosto_maukkaat_kasvattaa_kassan_arvoja(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttimaksu_edulliset_toimii_kun_rahaa_tarpeeksi(self):
        kortti = Maksukortti(500)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 260)

    def test_korttimaksu_edulliset_toimii_kun_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 100)
    
    def test_korttimaksu_maukkaat_toimii_kun_rahaa_tarpeeksi(self):
        kortti = Maksukortti(500)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 100)
    
    def test_korttimaksu_maukkaat_toimii_kun_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(100)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 100)

    def test_kortille_lataus_toimii(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)
        self.assertEqual(kortti.saldo, 200)

    def test_kortille_lataus_ei_toimi_negatiivisella_summalla(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    
