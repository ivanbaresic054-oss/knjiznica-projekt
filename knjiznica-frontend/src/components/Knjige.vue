<script setup>
import { ref, computed } from 'vue'

// ================================
// PODACI
// ================================

const knjige = ref([])
const autori = ref([])

const prikaziKnjige = ref(false)

const pretraga = ref('')
const trenutnaStranica = ref(1)
const poStranici = 5

const novaKnjiga = ref({
  naslov: '',
  godina: '',
  zanr: '',
  autor_id: null
})


// ================================
// PRETRAGA
// ================================

const filtriraneKnjige = computed(() => {

  const tekst = pretraga.value
    .toLowerCase()
    .trim()

  if (!tekst) {
    return knjige.value
  }

  return knjige.value.filter(knjiga => {

    const naslov = knjiga.naslov || ''
    const godina = String(knjiga.godina || '')
    const zanr = knjiga.zanr || ''
    const autor = knjiga.autor || ''

    return (
      naslov.toLowerCase().includes(tekst) ||
      godina.toLowerCase().includes(tekst) ||
      zanr.toLowerCase().includes(tekst) ||
      autor.toLowerCase().includes(tekst)
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
      filtriraneKnjige.value.length /
      poStranici
    )
  )
})


const prikazaneKnjige = computed(() => {

  const pocetak =
    (trenutnaStranica.value - 1) *
    poStranici

  const kraj =
    pocetak + poStranici

  return filtriraneKnjige.value.slice(
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

  } catch (greska) {

    console.error(
      'Greška pri učitavanju autora:',
      greska
    )
  }
}


// ================================
// UCITAJ KNJIGE
// ================================

async function ucitajKnjige() {

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/knjige'
    )

    knjige.value = await odgovor.json()

    await ucitajAutore()

    prikaziKnjige.value = true

  } catch (greska) {

    console.error(
      'Greška pri učitavanju knjiga:',
      greska
    )
  }
}


// Autori trebaju odmah za dropdown
ucitajAutore()


// ================================
// DODAJ KNJIGU
// ================================

async function dodajKnjigu() {

  if (
    !novaKnjiga.value.naslov ||
    !novaKnjiga.value.godina ||
    !novaKnjiga.value.zanr ||
    !novaKnjiga.value.autor_id
  ) {

    alert(
      'Naslov, godina, žanr i autor su obavezni.'
    )

    return
  }


  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/knjige',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({

          naslov:
            novaKnjiga.value.naslov,

          godina:
            Number(novaKnjiga.value.godina),

          zanr:
            novaKnjiga.value.zanr,

          autor_id:
            novaKnjiga.value.autor_id
        })
      }
    )


    if (odgovor.ok) {

      novaKnjiga.value = {
        naslov: '',
        godina: '',
        zanr: '',
        autor_id: null
      }

      await ucitajKnjige()
    }

  } catch (greska) {

    console.error(
      'Greška pri dodavanju knjige:',
      greska
    )
  }
}


// ================================
// UREDI KNJIGU
// ================================

async function urediKnjigu(knjiga) {

  const naslov = prompt(
    'Unesi novi naslov:',
    knjiga.naslov
  )

  if (naslov === null) return


  const godina = prompt(
    'Unesi novu godinu izdanja:',
    knjiga.godina
  )

  if (godina === null) return


  const zanr = prompt(
    'Unesi novi žanr:',
    knjiga.zanr || ''
  )

  if (zanr === null) return


  if (
    naslov.trim() === '' ||
    godina.trim() === '' ||
    zanr.trim() === ''
  ) {

    alert(
      'Naslov, godina i žanr ne mogu biti prazni.'
    )

    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/knjige/${knjiga.id}`,
      {
        method: 'PUT',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({

          naslov: naslov,

          godina:
            Number(godina),

          zanr: zanr,

          autor_id:
            knjiga.autor_id
        })
      }
    )


    if (odgovor.ok) {
      await ucitajKnjige()
    }

  } catch (greska) {

    console.error(
      'Greška pri uređivanju knjige:',
      greska
    )
  }
}


// ================================
// OBRISI KNJIGU
// ================================

async function obrisiKnjigu(id) {

  const potvrda = confirm(
    'Jeste li sigurni da želite obrisati knjigu?'
  )

  if (!potvrda) {
    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/knjige/${id}`,
      {
        method: 'DELETE'
      }
    )


    if (odgovor.ok) {

      await ucitajKnjige()

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
      'Greška pri brisanju knjige:',
      greska
    )
  }
}

</script>


<template>

  <div>

    <!-- ================================ -->
    <!-- KNJIGE -->
    <!-- ================================ -->

    <v-card>

      <v-card-title>
        Knjige
      </v-card-title>

      <v-card-text>
        Pregled i upravljanje knjigama.
      </v-card-text>

      <v-card-actions>

        <v-btn
          color="primary"
          @click="ucitajKnjige"
        >
          Prikaži knjige
        </v-btn>

      </v-card-actions>

    </v-card>


    <!-- ================================ -->
    <!-- DODAJ KNJIGU -->
    <!-- ================================ -->

    <v-card class="mt-8">

      <v-card-title>
        Dodaj knjigu
      </v-card-title>

      <v-card-text>

        <v-text-field
          v-model="novaKnjiga.naslov"
          label="Naslov knjige"
        />


        <v-text-field
          v-model="novaKnjiga.godina"
          label="Godina izdanja"
          type="number"
        />


        <v-text-field
          v-model="novaKnjiga.zanr"
          label="Žanr"
        />


        <v-select
          v-model="novaKnjiga.autor_id"
          :items="autori"
          item-title="prezime"
          item-value="id"
          label="Autor"
        />


        <v-btn
          color="primary"
          @click="dodajKnjigu"
        >
          Dodaj knjigu
        </v-btn>

      </v-card-text>

    </v-card>


    <!-- ================================ -->
    <!-- POPIS KNJIGA -->
    <!-- ================================ -->

    <v-card
      v-if="prikaziKnjige"
      class="mt-8 mb-8"
    >

      <v-card-title>
        Popis knjiga
      </v-card-title>


      <!-- PRETRAGA -->

      <v-card-text>

        <v-text-field
          v-model="pretraga"
          label="Pretraži knjige"
          placeholder="Naslov, godina, žanr ili autor..."
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

            <th>
              Naslov
            </th>

            <th>
              Godina
            </th>

            <th>
              Žanr
            </th>

            <th>
              Autor
            </th>

            <th>
              Akcije
            </th>

          </tr>

        </thead>


        <tbody>

          <tr
            v-for="knjiga in prikazaneKnjige"
            :key="knjiga.id"
          >

            <td>
              {{ knjiga.id }}
            </td>


            <td>
              {{ knjiga.naslov }}
            </td>


            <td>
              {{ knjiga.godina }}
            </td>


            <td>
              {{ knjiga.zanr }}
            </td>


            <td>
              {{ knjiga.autor }}
            </td>


            <td>

              <v-btn
                size="small"
                color="primary"
                class="mr-2"
                @click="urediKnjigu(knjiga)"
              >
                Uredi
              </v-btn>


              <v-btn
                size="small"
                color="error"
                @click="obrisiKnjigu(knjiga.id)"
              >
                Obriši
              </v-btn>

            </td>

          </tr>


          <!-- NEMA REZULTATA -->

          <tr
            v-if="filtriraneKnjige.length === 0"
          >

            <td
              colspan="6"
              class="text-center pa-6"
            >

              Nema pronađenih knjiga.

            </td>

          </tr>

        </tbody>

      </v-table>


      <!-- ================================ -->
      <!-- PAGINACIJA -->
      <!-- ================================ -->

      <v-card-text
        v-if="filtriraneKnjige.length > 0"
      >

        <div class="text-center">

          <div class="mb-2">

            Ukupno knjiga:

            <strong>
              {{ filtriraneKnjige.length }}
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