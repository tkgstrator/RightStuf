<script setup lang="ts">
import { IonPage, IonToolbar, IonTitle, IonContent, IonGrid, IonRow, IonCol, IonSearchbar, IonRadioGroup, IonRadio, IonSelect, IonSelectOption } from '@ionic/vue';
import items from '@/assets/20230818/items-pre-order.json';
import ProductItem from '@/components/ProductItem.vue';
import { Ref, ref } from 'vue';
import IonHeader from '@/components/IonHeader.vue';

const search: Ref<string> = ref('');
</script>

<template>
  <IonPage>
    <IonHeader :search="search">Pre order</IonHeader>
    <IonContent>
      <IonGrid>
        <IonRow>
          <template
            v-for="item in items.filter((item) => search === '' ? true : item.displayname.toLowerCase().includes(search))"
            :key="item.internalId">
            <IonCol size="2" size-xs="12" size-sm="6" size-md="4" size-lg="3" size-xl="3">
              <ProductItem :item="item" />
            </IonCol>
          </template>
        </IonRow>
      </IonGrid>
    </IonContent>
  </IonPage>
</template>
