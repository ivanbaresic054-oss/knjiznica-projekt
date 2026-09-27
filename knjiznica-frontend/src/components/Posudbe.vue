<script setup>
import { ref, computed } from 'vue'

// ================================
// PODACI
// ================================

const posudbe = ref([])
const knjige = ref([])
const clanovi = ref([])

const prikaziPosudbe = ref(false)

const pretraga = ref('')
const trenutnaStranica = ref(1)
const poStranici = 5

const novaPosudba = ref({
  datum_posudbe: '',
  datum_povrata: '',
  status: 'aktivna',
  knjiga_id: null,
  clan_id: null
})


// ================================
// PRETRAGA
// ================================

const filtriranePosudbe = computed(() => {

  const tekst = pretraga.value
    .toLowerCase()
    .trim()

  if (!tekst) {
    return posudbe.value
  }

  return posudbe.value.filter(posudba => {

    const knjiga = posudba.knjiga || ''
    const clan = posudba.clan || ''
    const datumPosudbe = posudba.datum_posudbe || ''
    const datumPovrata = posudba.datum_povrata || ''
    const status = posudba.status || ''

    return (
      knjiga.toLowerCase().includes(tekst) ||
      clan.toLowerCase().includes(tekst) ||
      datumPosudbe.toLowerCase().includes(tekst) ||
      datumPovrata.toLowerCase().includes(tekst) ||
      status.toLowerCase().includes(tekst)
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
      filtriranePosudbe.value.length /
      poStranici
    )
  )
})


const prikazanePosudbe = computed(() => {

  const pocetak =
    (trenutnaStranica.value - 1) *
    poStranici

  const kraj =
    pocetak + poStranici

  return filtriranePosudbe.value.slice(
    pocetak,
    kraj
  )
})


function resetirajStranicu() {
  trenutnaStranica.value = 1
}


// ================================
// CLANOVI ZA DROPDOWN
// ================================

const clanoviZaOdabir = computed(() => {

  return clanovi.value.map(clan => ({
    id: clan.id,
    naziv: `${clan.ime} ${clan.prezime}`
  }))
})


// ================================
// UCITAJ KNJIGE
// ================================

async function ucitajKnjige() {

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/knjige'
    )

    knjige.value = await odgovor.json()

  } catch (greska) {

    console.error(
      'Greška pri učitavanju knjiga:',
      greska
    )
  }
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

  } catch (greska) {

    console.error(
      'Greška pri učitavanju članova:',
      greska
    )
  }
}


// ================================
// UCITAJ POSUDBE
// ================================

async function ucitajPosudbe() {

  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/posudbe'
    )

    posudbe.value = await odgovor.json()

    await ucitajKnjige()
    await ucitajClanove()

    prikaziPosudbe.value = true

  } catch (greska) {

    console.error(
      'Greška pri učitavanju posudbi:',
      greska
    )
  }
}


// Odmah trebamo knjige i clanove
// zbog dropdown izbornika

ucitajKnjige()
ucitajClanove()


// ================================
// DODAJ POSUDBU
// ================================

async function dodajPosudbu() {

  if (
    !novaPosudba.value.knjiga_id ||
    !novaPosudba.value.clan_id ||
    !novaPosudba.value.datum_posudbe
  ) {

    alert(
      'Knjiga, član i datum posudbe su obavezni.'
    )

    return
  }


  try {

    const odgovor = await fetch(
      'http://127.0.0.1:5000/api/posudbe',
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({

          datum_posudbe:
            novaPosudba.value.datum_posudbe,

          datum_povrata:
            novaPosudba.value.datum_povrata || null,

          status:
            novaPosudba.value.status,

          knjiga_id:
            novaPosudba.value.knjiga_id,

          clan_id:
            novaPosudba.value.clan_id
        })
      }
    )


    if (odgovor.ok) {

      novaPosudba.value = {
        datum_posudbe: '',
        datum_povrata: '',
        status: 'aktivna',
        knjiga_id: null,
        clan_id: null
      }

      await ucitajPosudbe()
    }

  } catch (greska) {

    console.error(
      'Greška pri dodavanju posudbe:',
      greska
    )
  }
}


// ================================
// UREDI POSUDBU
// ================================

async function urediPosudbu(posudba) {

  const datumPosudbe = prompt(
    'Unesi datum posudbe:',
    posudba.datum_posudbe
  )

  if (datumPosudbe === null) return


  const datumPovrata = prompt(
    'Unesi datum povrata:',
    posudba.datum_povrata || ''
  )

  if (datumPovrata === null) return


  const status = prompt(
    'Unesi status (aktivna/vracena):',
    posudba.status
  )

  if (status === null) return


  if (datumPosudbe.trim() === '') {

    alert(
      'Datum posudbe ne može biti prazan.'
    )

    return
  }


  if (
    status !== 'aktivna' &&
    status !== 'vracena'
  ) {

    alert(
      'Status mora biti "aktivna" ili "vracena".'
    )

    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/posudbe/${posudba.id}`,
      {
        method: 'PUT',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({

          datum_posudbe:
            datumPosudbe,

          datum_povrata:
            datumPovrata === ''
              ? null
              : datumPovrata,

          status:
            status,

          knjiga_id:
            posudba.knjiga_id,

          clan_id:
            posudba.clan_id
        })
      }
    )


    if (odgovor.ok) {
      await ucitajPosudbe()
    }

  } catch (greska) {

    console.error(
      'Greška pri uređivanju posudbe:',
      greska
    )
  }
}


// ================================
// OBRISI POSUDBU
// ================================

async function obrisiPosudbu(id) {

  const potvrda = confirm(
    'Jeste li sigurni da želite obrisati posudbu?'
  )

  if (!potvrda) {
    return
  }


  try {

    const odgovor = await fetch(
      `http://127.0.0.1:5000/api/posudbe/${id}`,
      {
        method: 'DELETE'
      }
    )


    if (odgovor.ok) {

      await ucitajPosudbe()

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
      'Greška pri brisanju posudbe:',
      greska
    )
  }
}

</script>


<template>

  <div>

    <!-- ================================ -->
    <!-- POSUDBE -->
    <!-- ================================ -->

    <v-card>

      <v-card-title>
        Posudbe
      </v-card-title>

      <v-card-text>
        Evidencija i upravljanje posudbama knjiga.
      </v-card-text>

      <v-card-actions>

        <v-btn
          color="primary"
          @click="ucitajPosudbe"
        >
          Prikaži posudbe
        </v-btn>

      </v-card-actions>

    </v-card>


    <!-- ================================ -->
    <!-- DODAJ POSUDBU -->
    <!-- ================================ -->

    <v-card class="mt-8">

      <v-card-title>
        Dodaj posudbu
      </v-card-title>

      <v-card-text>

        <!-- KNJIGA -->

        <v-select
          v-model="novaPosudba.knjiga_id"
          :items="knjige"
          item-title="naslov"
          item-value="id"
          label="Knjiga"
        />


        <!-- CLAN -->

        <v-select
          v-model="novaPosudba.clan_id"
          :items="clanoviZaOdabir"
          item-title="naziv"
          item-value="id"
          label="Član"
        />


        <!-- DATUM POSUDBE -->

        <v-text-field
          v-model="novaPosudba.datum_posudbe"
          label="Datum posudbe"
          type="date"
        />


        <!-- DATUM POVRATA -->

        <v-text-field
          v-model="novaPosudba.datum_povrata"
          label="Datum povrata"
          type="date"
        />


        <!-- STATUS -->

        <v-select
          v-model="novaPosudba.status"
          :items="['aktivna', 'vracena']"
          label="Status"
        />


        <v-btn
          color="primary"
          @click="dodajPosudbu"
        >
          Dodaj posudbu
        </v-btn>

      </v-card-text>

    </v-card>


    <!-- ================================ -->
    <!-- POPIS POSUDBI -->
    <!-- ================================ -->

    <v-card
      v-if="prikaziPosudbe"
      class="mt-8 mb-8"
    >

      <v-card-title>
        Popis posudbi
      </v-card-title>


      <!-- PRETRAGA -->

      <v-card-text>

        <v-text-field
          v-model="pretraga"
          label="Pretraži posudbe"
          placeholder="Knjiga, član, datum ili status..."
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
            <th>Knjiga</th>
            <th>Član</th>
            <th>Datum posudbe</th>
            <th>Datum povrata</th>
            <th>Status</th>
            <th>Akcije</th>
          </tr>

        </thead>


        <tbody>

          <tr
            v-for="posudba in prikazanePosudbe"
            :key="posudba.id"
          >

            <td>
              {{ posudba.id }}
            </td>


            <td>
              {{ posudba.knjiga }}
            </td>


            <td>
              {{ posudba.clan }}
            </td>


            <td>
              {{ posudba.datum_posudbe }}
            </td>


            <td>
              {{ posudba.datum_povrata || '-' }}
            </td>


            <td>

              <v-chip
                v-if="posudba.status === 'aktivna'"
                color="warning"
              >
                Aktivna
              </v-chip>


              <v-chip
                v-else
                color="success"
              >
                Vraćena
              </v-chip>

            </td>


            <td>

              <v-btn
                size="small"
                color="primary"
                class="mr-2"
                @click="urediPosudbu(posudba)"
              >
                Uredi
              </v-btn>


              <v-btn
                size="small"
                color="error"
                @click="obrisiPosudbu(posudba.id)"
              >
                Obriši
              </v-btn>

            </td>

          </tr>


          <!-- NEMA REZULTATA -->

          <tr
            v-if="filtriranePosudbe.length === 0"
          >

            <td
              colspan="7"
              class="text-center pa-6"
            >
              Nema pronađenih posudbi.
            </td>

          </tr>

        </tbody>

      </v-table>


      <!-- ================================ -->
      <!-- PAGINACIJA -->
      <!-- ================================ -->

      <v-card-text
        v-if="filtriranePosudbe.length > 0"
      >

        <div class="text-center">

          <div class="mb-2">

            Ukupno posudbi:

            <strong>
              {{ filtriranePosudbe.length }}
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