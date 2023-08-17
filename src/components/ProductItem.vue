<script setup lang="ts">
import { Item } from '@/dto/right.dto';
import { IonBadge, IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle, IonChip, IonCol, IonGrid, IonIcon, IonImg, IonItem, IonItemDivider, IonLabel, IonRow, IonText } from '@ionic/vue';
import { PropType } from 'vue';
import { languageOutline, checkmarkOutline } from 'ionicons/icons';
import dayjs from 'dayjs';

defineProps({
  item: {
    type: Object as PropType<Item>,
    required: true
  }
})
</script>

<template>
  <IonCard>
    <IonCardHeader>
      <IonImg :src="item.image_urls.slice(-1)[0]"></IonImg>
      <!-- <img :src="item.image_urls.slice(-1)[0]" /> -->
      <IonCardTitle>{{ item.displayname.split('Blu-ray')[0] }}</IonCardTitle>
      <!-- <IonCardSubtitle>{{ item.displayname }}</IonCardSubtitle> -->
    </IonCardHeader>
    <IonCardContent>
      <IonGrid>
        <IonRow>
          <IonCol>
            <IonLabel class="price">{{ item.online_price }}</IonLabel>
          </IonCol>
          <IonCol class="ion-align-self-baseline">
            <IonLabel class="date">{{ dayjs(item.release_date).format("YYYY/MM/DD") }}</IonLabel>
          </IonCol>
        </IonRow>
      </IonGrid>
    </IonCardContent>
  </IonCard>
</template>

<style scoped lang="scss">
ion-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

ion-card-title {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 38.39px;
  font-size: 16px;
}

ion-label {
  font-size: 16px;
  text-align: right;
}

ion-card-content {
  ion-grid {
    padding: 0px;
  }

  ion-row {
    padding: 0px;
  }

  ion-col {
    padding: 0px;
  }
}

ion-col.md:last-child {
  text-align: right;
}

ion-col.ios:last-child {
  text-align: right;
}

ion-card-header {
  padding-bottom: 4px;
}

ion-icon {
  // font-size: 1.5rem;
}

ion-card {
  margin: 2px;
}

.price::before {
  content: '$';
  margin-right: 2px;
}
</style>
