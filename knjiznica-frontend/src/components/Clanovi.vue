<script setup>
import { ref, computed } from 'vue'

// ================================
// PODACI
// ================================

const clanovi = ref([])
const prikaziClanove = ref(false)

const pretraga = ref('')
const trenutnaStranica = ref(1)
const poStranici = 5

const noviClan = ref({
  ime: '',
  prezime: '',
  email: '',
  telefon: ''
})


// ================================
// PRETRAGA
// ================================

const filtriraniClanovi = computed(() => {

  const tekst = pretraga.value
    .toLowerCase()
    .trim()

  if (!tekst) {
    return clanovi.value
  }

  return clanovi.value.filter(clan => {

    const ime = clan.ime || ''
    const prezime = clan.prezime || ''
    const email = clan.email || ''
    const telefon = clan.telefon || ''

    return (
      ime.toLowerCase().includes(tekst) ||
      prezime.toLowerCase().includes(tekst) ||
      email.toLowerCase().includes(tekst) ||
      telefon.toLowerCase().includes(tekst)
    )
  })
})


// ================================
// PAGINACIJA
// ================================

const brojStranica = computed(() => {

  return Math.max(
    1,
    Math.ceil(
      filtriraniClanovi.value.length /
      poStranici
    )
  )
})


const prikazaniClanovi = computed(() => {

  const pocetak =
    (trenutnaStranica.value - 1) *
    poStranici

  const kraj =
    pocetak + poStranici

  return filtriraniClanovi.value.slice(
    pocetak,
    kraj
  )
})


function resetirajStranicu() {
  trenutnaStranica.value = 1
}


// ================================
// UCITAJ CLANOVE
// ================================

async function ucitajClanove() {

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/clanovi'
    )

    clanovi.value = await odgovor.json()

    prikaziClanove.value = true

  } catch (greska) {

    console.error(
      'Greška pri učitavanju članova:',
      greska
    )
  }
}


// ================================
// DODAJ CLANA
// ================================

async function dodajClana() {

  if (
    !noviClan.value.ime ||
    !noviClan.value.prezime
  ) {

    alert(
      'Ime i prezime su obavezni.'
    )

    return
  }


  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/clanovi',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify(
          noviClan.value
        )
      }
    )


    if (odgovor.ok) {

      noviClan.value = {
        ime: '',
        prezime: '',
        email: '',
        telefon: ''
      }

      await ucitajClanove()
    }

  } catch (greska) {

    console.error(
      'Greška pri dodavanju člana:',
      greska
    )
  }
}


// ================================
// UREDI CLANA
// ================================

async function urediClana(clan) {

  const ime = prompt(
    'Unesi novo ime:',
    clan.ime
  )

  if (ime === null) return


  const prezime = prompt(
    'Unesi novo prezime:',
    clan.prezime
  )

  if (prezime === null) return


  const email = prompt(
    'Unesi novi email:',
    clan.email || ''
  )

  if (email === null) return


  const telefon = prompt(
    'Unesi novi telefon:',
    clan.telefon || ''
  )

  if (telefon === null) return


  if (
    ime.trim() === '' ||
    prezime.trim() === ''
  ) {

    alert(
      'Ime i prezime ne mogu biti prazni.'
    )

    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/clanovi/${clan.id}`,
      {
        method: 'PUT',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          ime: ime,
          prezime: prezime,
          email: email,
          telefon: telefon
        })
      }
    )


    if (odgovor.ok) {
      await ucitajClanove()
    }

  } catch (greska) {

    console.error(
      'Greška pri uređivanju člana:',
      greska
    )
  }
}


// ================================
// OBRISI CLANA
// ================================

async function obrisiClana(id) {

  const potvrda = confirm(
    'Jeste li sigurni da želite obrisati člana?'
  )

  if (!potvrda) {
    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/clanovi/${id}`,
      {
        method: 'DELETE'
      }
    )


    if (odgovor.ok) {

      await ucitajClanove()

      if (
        trenutnaStranica.value >
        brojStranica.value
      ) {

        trenutnaStranica.value =
          brojStranica.value
      }
    }

  } catch (greska) {

    console.error(
      'Greška pri brisanju člana:',
      greska
    )
  }
}

</script>


<template>

  <div>

    <!-- ================================ -->
    <!-- CLANOVI -->
    <!-- ================================ -->

    <v-card>

      <v-card-title>
        Članovi
      </v-card-title>

      <v-card-text>
        Pregled i upravljanje članovima knjižnice.
      </v-card-text>

      <v-card-actions>

        <v-btn
          color="primary"
          @click="ucitajClanove"
        >
          Prikaži članove
        </v-btn>

      </v-card-actions>

    </v-card>


    <!-- ================================ -->
    <!-- DODAJ CLANA -->
    <!-- ================================ -->

    <v-card class="mt-8">

      <v-card-title>
        Dodaj člana
      </v-card-title>

      <v-card-text>

        <v-text-field
          v-model="noviClan.ime"
          label="Ime"
        />


        <v-text-field
          v-model="noviClan.prezime"
          label="Prezime"
        />


        <v-text-field
          v-model="noviClan.email"
          label="Email"
          type="email"
        />


        <v-text-field
          v-model="noviClan.telefon"
          label="Telefon"
        />


        <v-btn
          color="primary"
          @click="dodajClana"
        >
          Dodaj člana
        </v-btn>

      </v-card-text>

    </v-card>


    <!-- ================================ -->
    <!-- POPIS CLANOVA -->
    <!-- ================================ -->

    <v-card
      v-if="prikaziClanove"
      class="mt-8 mb-8"
    >

      <v-card-title>
        Popis članova
      </v-card-title>


      <!-- PRETRAGA -->

      <v-card-text>

        <v-text-field
          v-model="pretraga"
          label="Pretraži članove"
          placeholder="Ime, prezime, email ili telefon..."
          prepend-inner-icon="mdi-magnify"
          clearable
          @input="resetirajStranicu"
          @click:clear="resetirajStranicu"
        />

      </v-card-text>


      <!-- TABLICA -->

      <v-table>

        <thead>

          <tr>
            <th>ID</th>
            <th>Ime</th>
            <th>Prezime</th>
            <th>Email</th>
            <th>Telefon</th>
            <th>Akcije</th>
          </tr>

        </thead>


        <tbody>

          <tr
            v-for="clan in prikazaniClanovi"
            :key="clan.id"
          >

            <td>
              {{ clan.id }}
            </td>

            <td>
              {{ clan.ime }}
            </td>

            <td>
              {{ clan.prezime }}
            </td>

            <td>
              {{ clan.email }}
            </td>

            <td>
              {{ clan.telefon }}
            </td>

            <td>

              <v-btn
                size="small"
                color="primary"
                class="mr-2"
                @click="urediClana(clan)"
              >
                Uredi
              </v-btn>


              <v-btn
                size="small"
                color="error"
                @click="obrisiClana(clan.id)"
              >
                Obriši
              </v-btn>

            </td>

          </tr>


          <!-- NEMA REZULTATA -->

          <tr
            v-if="filtriraniClanovi.length === 0"
          >

            <td
              colspan="6"
              class="text-center pa-6"
            >
              Nema pronađenih članova.
            </td>

          </tr>

        </tbody>

      </v-table>


      <!-- ================================ -->
      <!-- PAGINACIJA -->
      <!-- ================================ -->

      <v-card-text
        v-if="filtriraniClanovi.length > 0"
      >

        <div class="text-center">

          <div class="mb-2">

            Ukupno članova:

            <strong>
              {{ filtriraniClanovi.length }}
            </strong>

          </div>


          <v-pagination
            v-model="trenutnaStranica"
            :length="brojStranica"
          />

        </div>

      </v-card-text>

    </v-card>

  </div>

</template>