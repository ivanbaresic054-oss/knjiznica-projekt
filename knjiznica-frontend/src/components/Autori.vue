<script setup>
import { ref, computed } from 'vue'

// ================================
// PODACI
// ================================

const autori = ref([])
const prikaziAutore = ref(false)

const pretraga = ref('')
const trenutnaStranica = ref(1)
const poStranici = 5

const noviAutor = ref({
  ime: '',
  prezime: '',
  drzava: ''
})


// ================================
// PRETRAGA
// ================================

const filtriraniAutori = computed(() => {

  const tekst = pretraga.value.toLowerCase().trim()

  if (!tekst) {
    return autori.value
  }

  return autori.value.filter(autor => {

    const ime = autor.ime || ''
    const prezime = autor.prezime || ''
    const drzava = autor.drzava || ''

    return (
      ime.toLowerCase().includes(tekst) ||
      prezime.toLowerCase().includes(tekst) ||
      drzava.toLowerCase().includes(tekst)
    )
  })
})


// ================================
// PAGINACIJA
// ================================

const brojStranica = computed(() => {
  return Math.max(
    1,
    Math.ceil(filtriraniAutori.value.length / poStranici)
  )
})


const prikazaniAutori = computed(() => {

  const pocetak =
    (trenutnaStranica.value - 1) * poStranici

  const kraj =
    pocetak + poStranici

  return filtriraniAutori.value.slice(
    pocetak,
    kraj
  )
})


function resetirajStranicu() {
  trenutnaStranica.value = 1
}


// ================================
// UCITAJ AUTORE
// ================================

async function ucitajAutore() {

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/autori'
    )

    autori.value = await odgovor.json()

    prikaziAutore.value = true

  } catch (greska) {

    console.error(
      'Greška pri učitavanju autora:',
      greska
    )
  }
}


// ================================
// DODAJ AUTORA
// ================================

async function dodajAutora() {

  if (
    !noviAutor.value.ime ||
    !noviAutor.value.prezime
  ) {
    alert('Ime i prezime su obavezni.')
    return
  }

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/autori',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify(
          noviAutor.value
        )
      }
    )

    if (odgovor.ok) {

      noviAutor.value = {
        ime: '',
        prezime: '',
        drzava: ''
      }

      await ucitajAutore()
    }

  } catch (greska) {

    console.error(
      'Greška pri dodavanju autora:',
      greska
    )
  }
}


// ================================
// UREDI AUTORA
// ================================

async function urediAutora(autor) {

  const ime = prompt(
    'Unesi novo ime:',
    autor.ime
  )

  if (ime === null) return


  const prezime = prompt(
    'Unesi novo prezime:',
    autor.prezime
  )

  if (prezime === null) return


  const drzava = prompt(
    'Unesi novu državu:',
    autor.drzava || ''
  )

  if (drzava === null) return


  if (
    ime.trim() === '' ||
    prezime.trim() === ''
  ) {
    alert('Ime i prezime ne mogu biti prazni.')
    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/autori/${autor.id}`,
      {
        method: 'PUT',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          ime: ime,
          prezime: prezime,
          drzava: drzava
        })
      }
    )

    if (odgovor.ok) {
      await ucitajAutore()
    }

  } catch (greska) {

    console.error(
      'Greška pri uređivanju autora:',
      greska
    )
  }
}


// ================================
// OBRISI AUTORA
// ================================

async function obrisiAutora(id) {

  const potvrda = confirm(
    'Jeste li sigurni da želite obrisati autora?'
  )

  if (!potvrda) {
    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/autori/${id}`,
      {
        method: 'DELETE'
      }
    )

    if (odgovor.ok) {

      await ucitajAutore()

      // Ako smo nakon brisanja ostali
      // na stranici koja vise ne postoji
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
      'Greška pri brisanju autora:',
      greska
    )
  }
}

</script>


<template>

  <div>

    <!-- ================================ -->
    <!-- AUTORI -->
    <!-- ================================ -->

    <v-card>

      <v-card-title>
        Autori
      </v-card-title>

      <v-card-text>
        Pregled i upravljanje autorima.
      </v-card-text>

      <v-card-actions>

        <v-btn
          color="primary"
          @click="ucitajAutore"
        >
          Prikaži autore
        </v-btn>

      </v-card-actions>

    </v-card>


    <!-- ================================ -->
    <!-- DODAJ AUTORA -->
    <!-- ================================ -->

    <v-card class="mt-8">

      <v-card-title>
        Dodaj autora
      </v-card-title>

      <v-card-text>

        <v-text-field
          v-model="noviAutor.ime"
          label="Ime"
        />

        <v-text-field
          v-model="noviAutor.prezime"
          label="Prezime"
        />

        <v-text-field
          v-model="noviAutor.drzava"
          label="Država"
        />

        <v-btn
          color="primary"
          @click="dodajAutora"
        >
          Dodaj autora
        </v-btn>

      </v-card-text>

    </v-card>


    <!-- ================================ -->
    <!-- POPIS AUTORA -->
    <!-- ================================ -->

    <v-card
      v-if="prikaziAutore"
      class="mt-8 mb-8"
    >

      <v-card-title>
        Popis autora
      </v-card-title>


      <!-- PRETRAGA -->

      <v-card-text>

        <v-text-field
          v-model="pretraga"
          label="Pretraži autore"
          placeholder="Ime, prezime ili država..."
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
            <th>Država</th>
            <th>Akcije</th>
          </tr>

        </thead>


        <tbody>

          <tr
            v-for="autor in prikazaniAutori"
            :key="autor.id"
          >

            <td>
              {{ autor.id }}
            </td>

            <td>
              {{ autor.ime }}
            </td>

            <td>
              {{ autor.prezime }}
            </td>

            <td>
              {{ autor.drzava }}
            </td>

            <td>

              <v-btn
                size="small"
                color="primary"
                class="mr-2"
                @click="urediAutora(autor)"
              >
                Uredi
              </v-btn>

              <v-btn
                size="small"
                color="error"
                @click="obrisiAutora(autor.id)"
              >
                Obriši
              </v-btn>

            </td>

          </tr>


          <!-- NEMA REZULTATA -->

          <tr
            v-if="filtriraniAutori.length === 0"
          >

            <td
              colspan="5"
              class="text-center pa-6"
            >
              Nema pronađenih autora.
            </td>

          </tr>

        </tbody>

      </v-table>


      <!-- PAGINACIJA -->

      <v-card-text
        v-if="filtriraniAutori.length > 0"
      >

        <div class="text-center">

          <div class="mb-2">

            Ukupno autora:
            <strong>
              {{ filtriraniAutori.length }}
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