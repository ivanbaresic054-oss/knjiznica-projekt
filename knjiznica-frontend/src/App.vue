<script setup>
import { ref } from 'vue'

import Autori from './components/Autori.vue'
import Knjige from './components/Knjige.vue'
import Clanovi from './components/Clanovi.vue'
import Posudbe from './components/Posudbe.vue'

// Pocetno prikazujemo autore
const aktivnaStranica = ref('autori')

function promijeniStranicu(stranica) {
  aktivnaStranica.value = stranica
}
</script>


<template>

  <v-app>

    <!-- =============================== -->
    <!-- GORNJA TRAKA -->
    <!-- =============================== -->

    <v-app-bar color="primary">

      <v-app-bar-title>
        📚 Knjižnica
      </v-app-bar-title>

      <!-- IZBORNIK -->

      <v-btn
        variant="text"
        @click="promijeniStranicu('autori')"
      >
        Autori
      </v-btn>


      <v-btn
        variant="text"
        @click="promijeniStranicu('knjige')"
      >
        Knjige
      </v-btn>


      <v-btn
        variant="text"
        @click="promijeniStranicu('clanovi')"
      >
        Članovi
      </v-btn>


      <v-btn
        variant="text"
        @click="promijeniStranicu('posudbe')"
      >
        Posudbe
      </v-btn>

    </v-app-bar>


    <!-- =============================== -->
    <!-- GLAVNI SADRZAJ -->
    <!-- =============================== -->

    <v-main>

      <v-container>

        <h1 class="text-h4 font-weight-bold mb-8">
          Sustav za upravljanje knjižnicom
        </h1>


        <!-- AUTORI -->

        <Autori
          v-if="aktivnaStranica === 'autori'"
        />


        <!-- KNJIGE -->

        <Knjige
          v-if="aktivnaStranica === 'knjige'"
        />


        <!-- CLANOVI -->

        <Clanovi
          v-if="aktivnaStranica === 'clanovi'"
        />


        <!-- POSUDBE -->

        <Posudbe
          v-if="aktivnaStranica === 'posudbe'"
        />

      </v-container>

    </v-main>

  </v-app>

</template>