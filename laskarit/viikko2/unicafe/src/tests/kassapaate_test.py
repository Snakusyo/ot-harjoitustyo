import unittest
from maksukortti import Maksukortti
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_rahamaara_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_myydyt_lounaat_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_edulliset_toimii_kun_rahaa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_kateisosto_maukkaat_toimii_kun_rahaa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisosto_edulliset_toimii_kun_rahaa_ei_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisosto_maukkaat_toimii_kun_rahaa_ei_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttiosto_edulliset_toimii_kun_rahaa_tarpeeksi(self):
        kortti = Maksukortti(250)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(kortti.saldo, 10)

    def test_korttiosto_maukkaat_toimii_kun_rahaa_tarpeeksi(self):
        kortti = Maksukortti(410)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), True)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(kortti.saldo, 10)

    def test_korttiosto_edulliset_toimii_kun_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(230)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(kortti.saldo, 230)

    def test_korttiosto_maukkaat_toimii_kun_rahaa_ei_tarpeeksi(self):
        kortti = Maksukortti(390)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(kortti.saldo, 390)

    def test_lataus_kortille_toimii_kun_summa_positiivinen(self):
        kortti = Maksukortti(500)
        self.kassapaate.lataa_rahaa_kortille(kortti, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100200)
        self.assertEqual(kortti.saldo, 700)

    def test_lataus_kortille__ei_onnistu_negatiivisella_summalla(self):
        kortti = Maksukortti(500)
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(kortti.saldo, 500)
