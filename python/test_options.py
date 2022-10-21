from base_options import BaseOptions


class TestOptions(BaseOptions):
    """This class includes test options.

    It also includes shared options defined in BaseOptions.
    """

    def initialize(self, parser):
        parser = BaseOptions.initialize(self, parser)  # define shared options
        parser.add_argument('--results_dir', type=str, default='./results/', help='saves results here.')
        parser.add_argument('--aspect_ratio', type=float, default=1.0, help='aspect ratio of result images')
        parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc')

        parser.add_argument('--input_nc_seg', type=int, default=1, help='input channel')
        parser.add_argument('--output_nc_seg', type=int, default=5, help='output class')

        # Dropout and Batchnorm has different behavioir during training and test.
        parser.add_argument('--eval', action='store_true', help='use eval mode during test time.')
        parser.add_argument('--num_test', type=int, default=50, help='how many test images to run')

        # add the option for SSL
        parser.add_argument('--save_dir', type=str, default='', help='the save dir used for save self supervise learning result')
        # rewrite devalue values
        parser.set_defaults(model='test')
        # To avoid cropping, the load_size should be the same as crop_size
        parser.set_defaults(load_size=parser.get_default('crop_size'))
        
        parser.preprcoess = 'None' # we do not need the preprocess stage
        parser.num_threads = 0   # test code only supports num_threads = 0
        parser.batch_size = 1    # test code only supports batch_size = 1
        parser.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
        parser.no_flip = True    # no flip; comment this line if results on flipped images are needed.
        self.isTrain = False
        return parser
