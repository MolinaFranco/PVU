Vue.component('pvu-button', {
  props: ['icon', 'url', 'disabled'],
  template: `
    <v-btn icon target="_blank" :href="url" :disabled="disabled">
      <v-icon>mdi-{{ icon }}</v-icon>
    </v-btn>
  `,
});

Vue.component('pvu-card', {
  props: ['title', 'color', 'img'],
  template: `
    <v-card :color="color" dark>
      <div class="my-t-4 d-flex flex-no-wrap justify-space-between">
        <div>
          <v-card-title class="headline">{{ title }}</v-card-title>
          <v-card-subtitle style="margin-bottom: 32px;">
            <slot name="content"></slot>
          </v-card-subtitle>
          <v-card-actions style="position: absolute; bottom: 0; padding: 16px;">
            <slot name="buttons"></slot>
          </v-card-actions>
        </div>
        <v-avatar class="ma-3 rounded" size="125" tile>
          <v-img :src="img"></v-img>
        </v-avatar>
      </div>
    </v-card>
  `,
});

Vue.component('pvu-div', {
  props: ['nCols', 'nRows'],
  data(instance) {
    return {
      defaultProps: {
        ...instance.$props,
      },
    };
  },
  methods: {
    onResize() {
      if (window.innerWidth < 600) {
        this.nCols = 1;
      } else {
        this.nCols = this.defaultProps.nCols;
      }
    },
  },
  created() {
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  computed: {
    style() {
      return {
        display: 'grid',
        gridTemplateColumns: `repeat(${this.nCols}, 1fr)`,
        gridTemplateRows: `repeat(${this.nRows}, 1fr)`,
        gridGap: '1rem',
        marginTop: '1rem',
      };
    },
  },
  template: `
    <div class="grid" :style="style">
      <slot></slot>
    </div>
  `,
});
