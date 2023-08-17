<script setup lang="ts">
import { IonPage, IonToolbar, IonTitle, IonContent, IonGrid, IonRow, IonCol, IonSearchbar, IonRadioGroup, IonRadio, IonSelect, IonSelectOption, IonList, IonInfiniteScroll, IonInfiniteScrollContent, InfiniteScrollCustomEvent, IonItemSliding } from '@ionic/vue';
import ProductItem from '@/components/ProductItem.vue';
import { PropType, Ref, onMounted, ref } from 'vue';
import IonHeader from '@/components/IonHeader.vue';
import { Item } from '@/dto/right.dto';
import { ContentType } from '@/dto/content';
import dayjs from 'dayjs';

const items: Ref<Item[]> = ref([])
const search: Ref<string> = ref('');
const current_time: string = dayjs().format("YYYYMMDD");

const props = defineProps({
  content: {
    type: String as PropType<ContentType>,
    required: true
  }
})

onMounted(async () => {
  items.value = (await import(`@/assets/${current_time}/${props.content}.json`)).default
})
</script>

<template>
  <IonPage>
    <IonHeader v-model="search">{{ props.content }}</IonHeader>
    <IonContent>
      <IonList>
        <IonGrid>
          <IonRow>
            <template
              v-for="item in items.filter((item) => search === '' ? true : item.displayname.toLowerCase().includes(search)).slice(0, 100)"
              :key="item.internalId">
              <IonCol size="2" size-xs="12" size-sm="6" size-md="4" size-lg="3" size-xl="3">
                <ProductItem :item="item" />
              </IonCol>
            </template>
          </IonRow>
        </IonGrid>
      </IonList>
    </IonContent>
  </IonPage>
</template>
